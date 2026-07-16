from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from .currency import DEFAULT_CURRENCY, normalize_currency


def _is_logged_in_user(request):
    return request.session.get('user') == 'user'


def _calculate_user_cart_totals(user_cart):
    from admin_app.models import SubCategory

    grand_total = 0
    vat = 0
    subcat_ids = []

    for subcat_id, item in user_cart.items():
        item['total'] = round(item['price'] * item['qty'], 2)
        item['subcat_id'] = subcat_id
        grand_total += item['total']
        subcat_ids.append(subcat_id)

    subcat_map = {
        str(subcat.id): subcat
        for subcat in SubCategory.objects.filter(id__in=subcat_ids).only('id', 'vat_status', 'tax_percentage')
    }

    for subcat_id, item in user_cart.items():
        subcat = subcat_map.get(str(subcat_id))
        if subcat and subcat.vat_status == 'include':
            rate = float(subcat.tax_percentage or 0)
            if rate > 0:
                vat += item['total'] * (rate / 100)

    return round(grand_total, 2), round(vat, 2)

@csrf_exempt
def user_checkout(request):
    from django.shortcuts import render, redirect
    if not _is_logged_in_user(request):
        return redirect('menu_page')
    user_cart = request.session.get('user_cart', {})
    grand_total, vat = _calculate_user_cart_totals(user_cart)
    delivery_charge = 0  # Placeholder, add logic for distance
    grand_total_with_vat = round(grand_total + vat + delivery_charge, 2)
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')
        user_cart = request.session.get('user_cart', {})
        grand_total, vat = _calculate_user_cart_totals(user_cart)
        delivery_charge = 0  # Placeholder, add logic for distance
        grand_total_with_vat = round(grand_total + vat + delivery_charge, 2)
        order_id = f"ORD{int(timezone.now().timestamp())}"  # Simple unique order id
        zipcode = request.POST.get('zipcode')
        # Save order details to UserOrder model
        from .models import UserOrder, UserOrderItem
        user_order = UserOrder.objects.create(
            name=name,
            address=address,
            zipcode=zipcode,
            phone=phone,
            payment_method=payment_method,
            delivered_place=address,
            price=grand_total,
            vat=vat,
            delivery_charge=delivery_charge,
            total_price=grand_total_with_vat
        )
        # Save each cart item to UserOrderItem
        for subcat_id, item in user_cart.items():
            UserOrderItem.objects.create(
                user_order=user_order,
                item_name=item.get('name', ''),
                quantity=item.get('qty', 1),
                price=item.get('price', 0)
            )
        request.session['user_cart'] = {}
        request.session['user_cart_count'] = 0
        # Print ESC/POS receipt
        from print_receipt import print_receipt
        receipt_order = {
            'restaurant_name': 'Kerala Street',
            'order_id': order_id,
            'full_name': name,
            'address': address,
            'zipcode': zipcode,
            'phone': phone,
            'payment_method': payment_method,
            'items': [
                {'name': item.get('name', ''), 'qty': item.get('qty', 1), 'price': item.get('price', 0)}
                for item in user_cart.values()
            ],
            'subtotal': grand_total,
            'vat': vat,
            'grand_total': grand_total_with_vat
        }
        usb_params = {'idVendor': 0x04b8, 'idProduct': 0x0202}
        try:
            print_receipt(receipt_order, printer_type='usb', usb_params=usb_params, paper_width=58)
        except Exception as e:
            print(f"Receipt printing failed: {e}")
        return render(request, 'ordersuccessful.html', {
            'order_id': order_id,
            'address': address,
            'phone': phone,
            'payment_method': payment_method,
            'full_name': name,
            'zipcode': zipcode,
            'user_cart': user_cart,
            'grand_total': grand_total,
            'vat': vat,
            'delivery_charge': delivery_charge,
            'grand_total_with_vat': grand_total_with_vat
        })
    return render(request, 'user_checkout.html', {
        'user_cart': user_cart,
        'grand_total': grand_total,
        'vat': vat,
        'delivery_charge': delivery_charge,
        'grand_total_with_vat': grand_total_with_vat
    })
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_user_cart(request):
    if not _is_logged_in_user(request):
        return redirect('menu_page')
    if request.method == 'POST':
        subcat_id = request.POST.get('subcat_id')
        qty = int(request.POST.get('qty', 1))
        user_cart = request.session.get('user_cart', {})
        if subcat_id in user_cart:
            user_cart[subcat_id]['qty'] = qty
            # Recalculate total
            user_cart[subcat_id]['total'] = round(user_cart[subcat_id]['price'] * qty, 2)
        request.session['user_cart'] = user_cart
        # Update cart count for notification badge
        total_items = sum(item['qty'] for item in user_cart.values())
        request.session['user_cart_count'] = total_items
    return redirect('user_cart')

@csrf_exempt
def remove_user_cart(request):
    if not _is_logged_in_user(request):
        return redirect('menu_page')
    if request.method == 'POST':
        subcat_id = request.POST.get('subcat_id')
        user_cart = request.session.get('user_cart', {})
        if subcat_id in user_cart:
            del user_cart[subcat_id]
        request.session['user_cart'] = user_cart
        # Update cart count for notification badge
        total_items = sum(item['qty'] for item in user_cart.values())
        request.session['user_cart_count'] = total_items
    return redirect('user_cart')
from django.shortcuts import render, HttpResponse, redirect
from .models import Reservation
from admin_app.models import maincategory, Category, SubCategory, chef


# Create your views here.
def menu_page(request):
    main_categories = maincategory.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.filter(is_available=True).select_related('category', 'category__main_category')
    return render(request, 'menu_page.html', {
        'main_categories': main_categories,
        'categories': categories,
        'subcategories': subcategories
    })


def about_page(request):
    return render(request, 'about.html')


def set_currency(request):
    currency = normalize_currency(request.GET.get('currency', DEFAULT_CURRENCY))
    request.session['currency'] = currency
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or 'index'
    return redirect(next_url)

def index(request):
    main_categories = maincategory.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.filter(is_available=True).select_related('category', 'category__main_category')
    from .models import HeroImage, GalleryImage, News
    hero_image = HeroImage.objects.last()
    gallery_images = GalleryImage.objects.all()
    news_items = News.objects.all().order_by('-id')[:4]  # Show latest 4 news
    return render(request, 'index.html', {
        'main_categories': main_categories,
        'categories': categories,
        'subcategories': subcategories,
        'hero_image': hero_image,
        'gallery_images': gallery_images,
        'news_items': news_items
    })


def _password_matches_and_upgrade(model_obj, raw_password):
    if not model_obj or not raw_password:
        return False
    if check_password(raw_password, model_obj.password):
        return True
    if model_obj.password == raw_password:
        model_obj.password = make_password(raw_password)
        model_obj.save(update_fields=['password'])
        return True
    return False

def login(request):
    if request.method == "POST":
        usermail = request.POST.get("usermail")
        userpassword = request.POST.get("userpassword")
        if (
            usermail == settings.ADMIN_LOGIN_EMAIL
            and check_password(userpassword, settings.ADMIN_LOGIN_PASSWORD_HASH)
        ):
            request.session['email'] = usermail
            request.session['name'] = 'admin'
            return redirect('admin_dashboard')
        elif usermail and userpassword:
            from admin_app.models import userdetails, chef
            user_obj = userdetails.objects.filter(email=usermail).first()
            if _password_matches_and_upgrade(user_obj, userpassword):
                if user_obj.is_team:
                    request.session['tid'] = user_obj.id
                    request.session['tname'] = user_obj.name
                    request.session['temail'] = user_obj.email
                    request.session['user'] = 'team'
                    request.session['email'] = user_obj.email  # For profile_view compatibility
                    return redirect('team_dashboard')
                else:
                    request.session['uid'] = user_obj.id
                    request.session['uname'] = user_obj.name
                    request.session['uemail'] = user_obj.email
                    request.session['user'] = 'user'
                    request.session['email'] = user_obj.email  # For profile_view compatibility
                    return render(request, 'index.html', {'status': 'user login success'})
            chef_obj = chef.objects.filter(email=usermail).first()
            if _password_matches_and_upgrade(chef_obj, userpassword):
                request.session['cid'] = chef_obj.id
                request.session['cname'] = chef_obj.name
                request.session['cemail'] = chef_obj.email
                request.session['user'] = 'chef'
                request.session['email'] = chef_obj.email
                return redirect('chef_dashboard')
        return render(request, 'login.html', {'status': 'login failed'})
    return render(request, "login.html")

def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect('index')

def book_table(request):
    import datetime
    today = datetime.date.today().isoformat()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        date = request.POST.get('date', '').strip()
        time = request.POST.get('time', '').strip()
        people = request.POST.get('guests', '').strip()
        message = request.POST.get('message', '').strip()

        errors = {}
        if not name:
            errors['name'] = 'Name is required.'
        if not email:
            errors['email'] = 'Email is required.'
        if not phone:
            errors['phone'] = 'Phone number is required.'
        elif not phone.isdigit() or len(phone) != 10:
            errors['phone'] = 'Phone number must be exactly 10 digits.'
        if not date:
            errors['date'] = 'Date is required.'
        if not time:
            errors['time'] = 'Time is required.'
        if not people:
            errors['guests'] = 'Number of guests is required.'
        else:
            try:
                if int(people) < 1:
                    errors['guests'] = 'At least 1 guest is required.'
            except ValueError:
                errors['guests'] = 'Guests must be a number.'
        if not message:
            errors['message'] = 'Message is required.'

        if errors:
            return render(request, 'book_table.html', {'errors': errors, 'name': name, 'email': email, 'phone': phone, 'date': date, 'time': time, 'guests': people, 'message': message, 'today': today})

        reservation = Reservation(name=name, email=email, phone=phone, date=date, time=time, people=people, message=message, is_new=True)
        reservation.save()
        return render(request, 'book_table.html', {'success': True, 'today': today})

    return render(request, 'book_table.html', {'today': today})


def user_cart(request):
    if not _is_logged_in_user(request):
        return redirect('menu_page')
    user_cart = request.session.get('user_cart', {})
    grand_total, vat = _calculate_user_cart_totals(user_cart)
    grand_total_with_vat = round(grand_total + vat, 2)
    return render(request, 'user_cart.html', {
        'user_cart': user_cart,
        'grand_total': grand_total,
        'vat': vat,
        'grand_total_with_vat': grand_total_with_vat
    })
from admin_app.models import SubCategory

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_to_user_cart(request):
    if not _is_logged_in_user(request):
        return redirect('menu_page')
    if request.method == 'POST':
        subcat_id = request.POST.get('subcat_id')
        qty = int(request.POST.get('qty', 1))
        # Get subcategory details
        try:
            subcat = SubCategory.objects.get(id=subcat_id)
        except SubCategory.DoesNotExist:
            return HttpResponse('Item not found', status=404)
        user_cart = request.session.get('user_cart', {})
        if subcat_id in user_cart:
            user_cart[subcat_id]['qty'] += qty
        else:
            user_cart[subcat_id] = {
                'name': subcat.name,
                'price': float(subcat.offer_price or subcat.price),
                'qty': qty,
                'image': subcat.image.url if subcat.image else '',
            }
        request.session['user_cart'] = user_cart
        # Update cart count for notification badge
        total_items = sum(item['qty'] for item in user_cart.values())
        request.session['user_cart_count'] = total_items
        return redirect('user_cart')