def cheforder_deliver(request, id):
    from team_app.models import Order, OrderItem
    from admin_app.models import SubCategory, SalesRevenue
    from .models import ChefDeliveredOrder
    from django.utils import timezone
    order = Order.objects.filter(id=id, status='Preparing').first()
    if order:
        items = order.items.all()
        subtotal = 0
        gst = 0
        for item in items:
            try:
                subcat = SubCategory.objects.get(name=item.name)
            except SubCategory.DoesNotExist:
                subcat = None
            item_price = item.total
            subtotal += item_price
            if subcat and subcat.vat_status == 'include':
                gst += item_price * 0.2
        total = subtotal + gst
        ChefDeliveredOrder.objects.create(
            order_id=order.id,
            table_number=order.table_number,
            placed_at=order.created_at,
            amount=subtotal,
            gst=gst,
            total=total
        )
        SalesRevenue.objects.create(
            order_id=order.id,
            delivered_at=timezone.now(),
            amount=subtotal,
            gst=gst,
            total=total
        )
        order.delete()
    return redirect('cheforder_accept', id=0)
# View to display all completed/delivered orders
from .models import ChefDeliveredOrder
from django.utils import timezone
from datetime import timedelta

def auto_delete_old_chefdelivered():
    two_years_ago = timezone.now() - timedelta(days=730)
    ChefDeliveredOrder.objects.filter(delivered_at__lt=two_years_ago).delete()

def chef_completed_orders(request):
    auto_delete_old_chefdelivered()
    completed_orders = ChefDeliveredOrder.objects.order_by('-delivered_at')
    return render(request, 'chef_completed_orders.html', {'orders': completed_orders})

from django.shortcuts import render,HttpResponse,redirect
from admin_app.models import maincategory, Category, SubCategory, chef
from team_app.models import Order
from team_app.models import OrderItem
from hotel.models import Reservation
from admin_app.models import userdetails
from admin_app.models import SalesRevenue

# Create your views here.

def load_chef_app(request):
    return HttpResponse('Chef app loaded successfully!')

def chef_profile(request):
    email = request.session.get('email')
    if email:
        from admin_app.models import chef
        chef_obj = chef.objects.filter(email=email).first()
        if chef_obj:
            context = {
                'name': chef_obj.name,
                'email': chef_obj.email,
                'specialty': chef_obj.specialty,
                'image': chef_obj.image,
                'phone': chef_obj.phone,
            }
            return render(request, 'chef_profile.html', context)
    return HttpResponse('Chef profile not found.', status=404)

def chef_dashboard(request):
    email = request.session.get('email')
    online_order_count = 0
    from hotel.models import AcceptedOrder
    online_order_count = AcceptedOrder.objects.count()
    pending_orders_count = 0
    pending_table_numbers = []
    from team_app.models import Order
    pending_orders = Order.objects.filter(status='Pending')
    pending_orders_count = pending_orders.count()
    pending_table_numbers = list(pending_orders.values_list('table_number', flat=True))
    online_order_request_count = 0
    online_order_requests = AcceptedOrder.objects.all()
    online_order_request_count = online_order_requests.count()
    if email:
        from admin_app.models import chef
        chef_obj = chef.objects.filter(email=email).first()
        if chef_obj:
            auto_delete_old_chefdelivered()
            # Get last 10 Pending, Preparing orders and completed orders
            from team_app.models import Order
            last_10_pending = Order.objects.filter(status='Pending').order_by('-created_at')[:10]
            last_10_preparing = Order.objects.filter(status='Preparing').order_by('-created_at')[:10]
            completed_orders = ChefDeliveredOrder.objects.order_by('-delivered_at')
            context = {
                'name': chef_obj.name,
                'email': chef_obj.email,
                'specialty': chef_obj.specialty,
                'image': chef_obj.image,
                'phone': chef_obj.phone,
                'last_10_pending': last_10_pending,
                'last_10_preparing': last_10_preparing,
                'completed_orders': completed_orders,
                'online_order_count': online_order_count,
                'pending_orders_count': pending_orders_count,
                'pending_table_numbers': pending_table_numbers,
                'online_order_request_count': online_order_request_count,
                    # Removed online_order_request_table_numbers from context as requested
            }
            return render(request, 'chef_dashboard.html', context)
    return HttpResponse('Chef dashboard not found.', status=404)


from team_app.models import Order
from admin_app.models import userdetails
def cheforder_request(request):
    # Get all orders (customize filter as needed)
    orders = Order.objects.filter(status='Pending').order_by('-created_at')
    # Attach userdetails to each order (assuming table_number is user name, adjust if needed)
    for order in orders:
        user = userdetails.objects.filter(name=order.table_number).first()
        order.userdetails = user
    return render(request, 'cheforder_request.html', {'orders': orders})

def cheforder_accept(request, id):
    order = Order.objects.filter(id=id).first()
    if order:
        order.status = 'Preparing'
        order.save()
        # Redirect to preparing page
        return redirect('cheforder_accept', id=0)
    # Show all preparing orders if not found
    preparing_orders = Order.objects.filter(status='Preparing').order_by('-created_at')
    return render(request, 'cheforder_accept.html', {'orders': preparing_orders})

def cheforder_delete(request, id):
    order = Order.objects.filter(id=id).first()
    if order:
        order.delete()
    return redirect('cheforder_request')

def cheforder_delivered(request, id):
    from .models import ChefDeliveredOrder
    order = Order.objects.filter(id=id).first()
    if order:
        items = order.items.all()
        subtotal = 0
        gst = 0
        for item in items:
            # Find the corresponding SubCategory for VAT check
            try:
                subcat = SubCategory.objects.get(name=item.name)
            except SubCategory.DoesNotExist:
                subcat = None
            item_price = item.total
            subtotal += item_price
            if subcat and subcat.vat_status == 'include':
                gst += item_price * 0.2
        total = subtotal + gst
        # Save to ChefDeliveredOrder
        ChefDeliveredOrder.objects.create(
            order_id=order.id,
            table_number=order.table_number,
            placed_at=order.created_at,
            amount=subtotal,
            gst=gst,
            total=total
        )
        # Save to SalesRevenue (admin_app)
        SalesRevenue.objects.create(
            order_id=order.id,
            delivered_at=timezone.now(),
            amount=subtotal,
            gst=gst,
            total=total
        )
        order.delete()
        # Redirect to delivered page so order disappears from delivered list
        return redirect('cheforder_delivered', id=0)
    # Show delivered orders from Order table
    delivered_orders = Order.objects.filter(status='Delivered').order_by('-created_at')
    orders_with_amount = []
    for dorder in delivered_orders:
        items = dorder.items.all()
        subtotal = sum([item.total for item in items])
        gst = subtotal * 0.2
        total = subtotal + gst
        orders_with_amount.append({
            'id': dorder.id,
            'table_number': dorder.table_number,
            'items': items,
            'created_at': dorder.created_at,
            'amount': subtotal,
            'gst': gst,
            'total': total
        })
    return render(request, 'cheforder_delivered.html', {'orders': orders_with_amount})

from django.shortcuts import render
from hotel.models import AcceptedOrder
from django.db import models

def chef_online_orders(request):
    auto_delete_old_accepted_orders()
    from hotel.models import AcceptedOrder
    approved_orders = AcceptedOrder.objects.all().order_by('-order_time')[:25]
    return render(request, 'all_approved_orders.html', {'approved_orders': approved_orders})

from django.shortcuts import render, redirect
from hotel.models import AcceptedOrder, AcceptedOrderItem

def chef_order_delivered(request, id):
    order = AcceptedOrder.objects.filter(id=id).first()
    items = AcceptedOrderItem.objects.filter(accepted_order=order)
    # Optionally, mark as delivered or remove from table
    # order.delete()  # Uncomment if you want to remove after printing
    return render(request, 'chef_order_print.html', {'order': order, 'items': items})

from django.utils import timezone
from datetime import timedelta

def auto_delete_old_accepted_orders():
    cutoff_date = timezone.now() - timedelta(days=732)
    from hotel.models import AcceptedOrder
    AcceptedOrder.objects.filter(order_time__lt=cutoff_date).delete()

from hotel.models import AcceptedOrder

def chef_online_order_revenue(request):
    # Calculate total online order revenue from AcceptedOrder
    import decimal
    from datetime import datetime, timedelta
    period = request.GET.get('period', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    orders = AcceptedOrder.objects.all()
    now = timezone.now()
    if period == 'daily':
        orders = orders.filter(order_time__date=now.date())
    elif period == '7days':
        orders = orders.filter(order_time__gte=now - timedelta(days=7))
    elif period == '1month':
        orders = orders.filter(order_time__gte=now - timedelta(days=30))
    elif period == '3months':
        orders = orders.filter(order_time__gte=now - timedelta(days=90))
    elif period == '6months':
        orders = orders.filter(order_time__gte=now - timedelta(days=180))
    elif period == '1year':
        orders = orders.filter(order_time__gte=now - timedelta(days=365))
    elif period == 'custom' and start_date and end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            orders = orders.filter(order_time__gte=start, order_time__lt=end)
        except Exception:
            pass
    orders = orders.order_by('-order_time')
    online_orders = []
    total_revenue = decimal.Decimal('0.0')
    subtotal_amount = decimal.Decimal('0.0')
    subtotal_gst = decimal.Decimal('0.0')
    for order in orders:
        gst = order.total_price * decimal.Decimal('0.2')
        total = order.total_price + gst
        subtotal_amount += order.total_price
        subtotal_gst += gst
        total_revenue += total
        online_orders.append({
            'id': order.id,
            'order_time': order.order_time,
            'total_price': order.total_price,
            'gst': gst,
            'total': total,
        })
    return render(request, 'online_order_revenue.html', {
        'total_revenue': total_revenue,
        'online_orders': online_orders,
        'subtotal_amount': subtotal_amount,
        'subtotal_gst': subtotal_gst,
        'period': period,
        'start_date': start_date,
        'end_date': end_date
    })

