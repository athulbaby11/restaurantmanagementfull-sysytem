from django.utils import timezone
from admin_app.models import SubCategory
from django.utils import timezone
from datetime import timedelta

def today_unavailable_items(request):
    today = timezone.now().date()
    # Assuming unavailable items are those with is_available=False and created/updated today
    unavailable_items = SubCategory.objects.filter(is_available=False)
    return render(request, 'unavailable_items.html', {'unavailable_items': unavailable_items, 'today': today})
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def preparing_order(request):
    if request.method == 'POST':
        order_id = request.GET.get('order_id')
        table_number = request.GET.get('table_number')
        order = Order.objects.filter(id=order_id).first()
        if order:
            order.status = 'Preparing'
            order.save()
        if table_number:
            return redirect('delivered_orders')
    return redirect('delivered_orders')

def delivered_orders(request):
    # Show all orders with status 'Preparing'
    preparing_orders = Order.objects.filter(status='Preparing').order_by('-created_at')
    return render(request, 'delivered_orders.html', {'preparing_orders': preparing_orders})

@csrf_exempt
def delete_order(request):
    if request.method == 'POST':
        order_id = request.GET.get('order_id')
        order = Order.objects.filter(id=order_id).first()
        if order:
            order.delete()
        return redirect('/delivered_orders/')
    return redirect('/delivered_orders/')

# Auto-delete OrderItems older than 7 days
def auto_delete_old_orderitems():
    cutoff = timezone.now() - timedelta(days=7)
    OrderItem.objects.filter(order__created_at__lt=cutoff).delete()

def all_pending_orders(request):
    auto_delete_old_orderitems()
    pending_orders = Order.objects.filter(status='Pending').order_by('-created_at')
    return render(request, 'all_pending_orders.html', {'pending_orders': pending_orders})

def all_approved_orders(request):
    auto_delete_old_orderitems()
    approved_orders = Order.objects.filter(status='Accepted').order_by('-created_at')
    return render(request, 'all_approved_orders.html', {'approved_orders': approved_orders})


def _is_team_user(request):
    if request.session.get('user') == 'team':
        return True
    if request.session.get('tid') or request.session.get('tname') or request.session.get('temail'):
        return True
    email = request.session.get('email')
    if email:
        return userdetails.objects.filter(email=email, is_team=True).exists()
    return False


def _is_logged_in_session(request):
    return bool(request.session.get('email'))


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@csrf_exempt
def remove_team_cart_item(request):
    if not _is_logged_in_session(request):
        return redirect('menu_page')
    if request.method == 'POST':
        subcat_id = request.POST.get('subcat_id')
        table_number = request.POST.get('table_number')
        team_carts = request.session.get('team_carts', {})
        if table_number and table_number in team_carts:
            cart = team_carts[table_number]
            if subcat_id in cart:
                del cart[subcat_id]
                # If cart is empty after removal, delete the table cart
                if not cart:
                    del team_carts[table_number]
                else:
                    team_carts[table_number] = cart
                request.session['team_carts'] = team_carts
            # Update team_cart notification badge
            total_items = sum(item['qty'] for cart in team_carts.values() for item in cart.values())
            if total_items > 0:
                request.session['team_cart'] = total_items
            elif 'team_cart' in request.session:
                del request.session['team_cart']
        return redirect('team_cart')
    return HttpResponse('Invalid request', status=400)
from django.shortcuts import render, HttpResponse, redirect
from django.shortcuts import render
from admin_app.models import userdetails
from admin_app.models import maincategory, Category
from admin_app.models import SubCategory
from hotel.models import Reservation
from .models import Order, OrderItem
# Create your views here.

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def place_order(request):
    if not _is_logged_in_session(request):
        return redirect('menu_page')
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        if not table_number:
            return HttpResponse('Table number is required.', status=400)
        table_number = str(table_number)
        team_carts = request.session.get('team_carts', {})
        cart = team_carts.get(table_number, {}) if table_number else {}
        if not cart:
            return HttpResponse('No items in cart for this table.', status=400)
        # Create Order
        order = Order.objects.create(table_number=table_number, status='Pending')
        order_items = []
        subtotal = 0
        vat = 0
        from admin_app.models import SubCategory
        for subcat_id, item in cart.items():
            item_total = item['price'] * item['qty']
            order_item = OrderItem.objects.create(
                order=order,
                name=item['name'],
                price=item['price'],
                qty=item['qty'],
                total=item_total
            )
            order_items.append(order_item)
            subtotal += item_total
            try:
                subcat = SubCategory.objects.get(id=subcat_id)
            except SubCategory.DoesNotExist:
                subcat = None
            if subcat and subcat.vat_status == 'include':
                rate = float(subcat.tax_percentage or 0)
                if rate > 0:
                    vat += item_total * (rate / 100)
        total = subtotal + vat

        # Persist totals on the order for reporting.
        order.subtotal = subtotal
        order.gst = vat
        order.total = total
        order.save(update_fields=['subtotal', 'gst', 'total'])

        # Remove cart for this table
        team_carts.pop(table_number, None)
        request.session['team_carts'] = team_carts
        request.session.modified = True

        # Update team_cart notification badge
        total_items = sum(item['qty'] for cart in team_carts.values() for item in cart.values())
        if total_items > 0:
            request.session['team_cart'] = total_items
        elif 'team_cart' in request.session:
            del request.session['team_cart']

        # Get logged-in user name for receipt.
        user_email = request.session.get('email')
        user_name = request.session.get('tname') or ''
        if user_email:
            try:
                user = userdetails.objects.get(email=user_email)
                user_name = user.name
            except userdetails.DoesNotExist:
                user_name = user_name or ''

        # Print waiter order receipt (optional if printer is unavailable).
        from hotel.settings import HOTEL_NAME
        from print_receipt import print_receipt
        receipt_order = {
            'restaurant_name': HOTEL_NAME if 'HOTEL_NAME' in dir() else 'Hotel',
            'order_placed_by': user_name,
            'table_number': table_number,
            'items': [
                {'name': item.name, 'qty': item.qty, 'price': item.price}
                for item in order_items
            ],
            'subtotal': subtotal,
            'vat': vat,
            'grand_total': total,
        }
        usb_params = {'idVendor': 0x04b8, 'idProduct': 0x0202}
        try:
            print_receipt(receipt_order, printer_type='usb', usb_params=usb_params, paper_width=58)
        except Exception as e:
            print(f"Receipt printing failed: {e}")

        context = {
            'table_number': table_number,
            'order_id': order.id,
            'order_items': order_items,
            'subtotal': subtotal,
            'vat': vat,
            'total': total,
            'grand_total_with_vat': total,
            'order_created_at': order.created_at,
            'grand_total': total,
            'order_placed_by': user_name,
        }
        return render(request, 'ordersuccessful.html', context)
    return HttpResponse('Invalid request', status=400)

def load_team_app(request):
    return HttpResponse("Team App Loaded Successfully")


def _calculate_team_cart_totals(cart):
    subtotal = 0
    vat = 0
    subcat_ids = [key for key in cart.keys()]
    subcat_map = {
        str(subcat.id): subcat
        for subcat in SubCategory.objects.filter(id__in=subcat_ids).only('id', 'vat_status', 'tax_percentage')
    }

    for key, item in cart.items():
        item_subtotal = item['price'] * item['qty']
        subtotal += item_subtotal
        subcat = subcat_map.get(str(key))
        if subcat and subcat.vat_status == 'include':
            rate = float(subcat.tax_percentage or 0)
            if rate > 0:
                vat += item_subtotal * (rate / 100)

    return subtotal, vat, subtotal + vat

def profile_view(request):
    # Get the logged-in user's email from session
    user_email = request.session.get('email')
    user = None
    debug_message = ''
    if user_email:
        try:
            user = userdetails.objects.get(email=user_email)
        except userdetails.DoesNotExist:
            debug_message = f"No user found with email: {user_email}"
    else:
        debug_message = "No email found in session."
    return render(request, 'profile_view.html', {'user': user, 'debug_message': debug_message})

def team_dashboard(request):
    if not _is_logged_in_session(request):
        return redirect('menu_page')
    table_numbers = list(range(1, 31))
    return render(request, 'team_dashboard.html', {'table_numbers': table_numbers})

def team_order_menu(request):
    if not _is_logged_in_session(request):
        return redirect('menu_page')
    table_number = request.session.get('team_table_number')
    if table_number:
        try:
            return redirect('order_view', table_number=int(table_number))
        except (TypeError, ValueError):
            return redirect('team_dashboard')
    return redirect('team_dashboard')

def order_view(request, table_number=None):
    if not _is_logged_in_session(request):
        return redirect('menu_page')
    if table_number:
        request.session['team_table_number'] = str(table_number)
    main_categories = maincategory.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.filter(is_available=True)
    return render(request, 'menu_page.html', {
        'main_categories': main_categories,
        'categories': categories,
        'subcategories': subcategories,
        'table_number': table_number,
        'team_mode': True,
    })

# Add to cart logic (POST)
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_to_team_cart(request):
    if not _is_logged_in_session(request):
        return redirect('menu_page')
    if request.method == 'POST':
        subcat_id = request.POST.get('subcat_id')
        qty = int(request.POST.get('qty', 1))
        table_number = request.POST.get('table_number') or request.session.get('team_table_number')
        if not table_number:
            return redirect('team_dashboard')
        table_number = str(table_number)
        request.session['team_table_number'] = table_number
        subcat_id = str(subcat_id)
        # Get subcategory details
        try:
            subcat = SubCategory.objects.get(id=subcat_id)
        except SubCategory.DoesNotExist:
            return HttpResponse('Item not found', status=404)
        team_carts = request.session.get('team_carts', {})
        if table_number:
            table_cart = team_carts.get(table_number, {})
            if subcat_id in table_cart:
                table_cart[subcat_id]['qty'] += qty
            else:
                table_cart[subcat_id] = {
                    'name': subcat.name,
                    'price': float(subcat.offer_price or subcat.price),
                    'qty': qty,
                    'image': subcat.image.url if subcat.image else '',
                }
            team_carts[table_number] = table_cart
            request.session['team_carts'] = team_carts
            request.session.modified = True
            # Update cart count for notification badge
            total_items = sum(item['qty'] for cart in team_carts.values() for item in cart.values())
            request.session['team_cart'] = total_items
            # After adding, return to the same table order page so the waiter can keep ordering.
            if table_number:
                return redirect('order_view', table_number=table_number)
            return redirect('team_dashboard')
    return HttpResponse('Invalid request', status=400)

def team_cart(request):
    if not _is_logged_in_session(request):
        return redirect('menu_page')
    auto_delete_old_orderitems()
    team_carts = request.session.get('team_carts', {})
    waiter_name = request.session.get('tname') or ''
    cart_totals = {}
    from .models import Order
    for table_num, cart in team_carts.items():
        cart_with_subtotals = {}
        for key, item in cart.items():
            item_copy = item.copy()
            item_copy['subtotal'] = item['price'] * item['qty']
            cart_with_subtotals[key] = item_copy
        total, vat, grand_total = _calculate_team_cart_totals(cart_with_subtotals)
        # Fetch latest order for this table
        latest_order = Order.objects.filter(table_number=table_num).order_by('-created_at').first()
        order_created_at = latest_order.created_at if latest_order else None
        cart_totals[table_num] = {
            'cart': cart_with_subtotals,
            'total': total,
            'vat': vat,
            'grand_total': grand_total,
            'order_created_at': order_created_at,
        }
    return render(request, 'team_cart.html', {
        'cart_totals': cart_totals,
        'waiter_name': waiter_name,
    })

def update_team_cart_item(request):
    if not _is_logged_in_session(request):
        return redirect('menu_page')
    team_carts = request.session.get('team_carts', {})
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        if table_number and table_number in team_carts:
            cart = team_carts[table_number]
            updated = False
            for key in list(cart.keys()):
                qty_str = request.POST.get(f'qty_{key}')
                if qty_str is not None:
                    qty = int(qty_str)
                    if qty > 0:
                        cart[key]['qty'] = qty
                        updated = True
                    else:
                        del cart[key]
                        updated = True
            # If cart is empty after update, delete the table cart
            if not cart:
                del team_carts[table_number]
            else:
                team_carts[table_number] = cart
            request.session['team_carts'] = team_carts
        # Update team_cart notification badge
        total_items = sum(item['qty'] for cart in team_carts.values() for item in cart.values())
        if total_items > 0:
            request.session['team_cart'] = total_items
        elif 'team_cart' in request.session:
            del request.session['team_cart']
        return redirect('team_cart')
    # GET: show update form for selected table
    table_number = request.GET.get('table_number')
    table_cart = team_carts.get(table_number, {}) if table_number else {}
    subtotal, vat, total = _calculate_team_cart_totals(table_cart)
    return render(request, 'team_cartupdate.html', {
        'table_number': table_number,
        'table_cart': table_cart,
        'subtotal': subtotal,
        'vat': vat,
        'total': total,
    })

