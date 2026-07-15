def all_approved_orders(request):
    from hotel.models import AcceptedOrder
    approved_orders = AcceptedOrder.objects.all().order_by('-order_time')
    return render(request, 'all_approved_orders.html', {'approved_orders': approved_orders})
from django.http import HttpResponseRedirect
from django.urls import reverse

def admin_online_order_accept(request, id):
    from hotel.models import UserOrder, AcceptedOrder, UserOrderItem, AcceptedOrderItem
    order = UserOrder.objects.filter(id=id).first()
    if order:
        # Copy order details to AcceptedOrder
        accepted_order = AcceptedOrder.objects.create(
            name=order.name,
            address=order.address,
            zipcode=order.zipcode,
            phone=order.phone,
            payment_method=order.payment_method,
            order_time=order.order_time,
            delivered_place=order.delivered_place,
            price=order.price,
            vat=order.vat,
            delivery_charge=order.delivery_charge,
            total_price=order.total_price
        )
        # Copy items to AcceptedOrderItem
        items = UserOrderItem.objects.filter(user_order=order)
        for item in items:
            AcceptedOrderItem.objects.create(
                accepted_order=accepted_order,
                item_name=item.item_name,
                quantity=item.quantity,
                price=item.price
            )
        # Delete items and order
        items.delete()
        order.delete()
    return HttpResponseRedirect(reverse('admin_online_orders'))

def admin_online_order_delete(request, id):
    if request.method == 'POST':
        from hotel.models import UserOrder
        order = UserOrder.objects.filter(id=id).first()
        if order:
            order.delete()
        return HttpResponseRedirect(reverse('admin_online_orders'))
from hotel.models import UserOrder

def admin_online_orders(request):
    online_orders = UserOrder.objects.filter(status="Pending").order_by('-order_time')
    online_order_count = online_orders.count()
    return render(request, 'admin_online_orders.html', {'online_orders': online_orders, 'online_order_count': online_order_count})

def admin_accepted_orders(request):
    accepted_orders = UserOrder.objects.filter(status="Accepted").order_by('-order_time')
    accepted_order_count = accepted_orders.count()
    return render(request, 'admin_accepted_orders.html', {'accepted_orders': accepted_orders, 'accepted_order_count': accepted_order_count})
def toggle_subcat_vat(request, id):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    from .models import SubCategory
    if request.method == 'POST':
        subcat = SubCategory.objects.get(id=id)
        # Cycle through VAT statuses
        if subcat.vat_status == 'not_include':
            subcat.vat_status = 'include'
        elif subcat.vat_status == 'include':
            subcat.vat_status = 'vatl_include'
        else:
            subcat.vat_status = 'not_include'
        subcat.save()
    return HttpResponseRedirect(reverse('subcat_view'))
from django.shortcuts import render ,HttpResponse
from django.shortcuts import render
from .models import userdetails ,maincategory,Category,SubCategory
from Chef_app.models import ChefDeliveredOrder
from team_app.models import Order
from .models import SalesRevenue,Expense
from django.utils import timezone
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from datetime import timedelta
from hotel.models import GalleryImage
from hotel.models import HeroImage
from hotel.models import News

# Create your views here.

def admin_news_list(request):
    news_items = News.objects.all()
    return render(request, 'admin_news_list.html', {'news_items': news_items})

def admin_news_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            News.objects.create(title=title, content=content)
            return render(request, 'admin_news_add.html', {'success': True})
    return render(request, 'admin_news_add.html')

def admin_news_edit(request, id):
    news_obj = get_object_or_404(News, id=id)
    if request.method == 'POST':
        news_obj.title = request.POST.get('title')
        news_obj.content = request.POST.get('content')
        news_obj.save()
        return render(request, 'admin_news_edit.html', {'news': news_obj, 'success': True})
    return render(request, 'admin_news_edit.html', {'news': news_obj})

def admin_news_delete(request, id):
    news_obj = get_object_or_404(News, id=id)
    news_obj.delete()
    return render(request, 'admin_news_list.html', {'news_items': News.objects.all(), 'deleted': True})
def admin_hero_list(request):
    images = HeroImage.objects.all()
    return render(request, 'admin_hero_list.html', {'images': images})

def admin_hero_add(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            # Use fixed values for headline and subheadline
            HeroImage.objects.create(
                image=image,
                headline='BOLD TASTE OF KERALA',
                subheadline='Now in Hounslow'
            )
            return render(request, 'admin_hero_add.html', {'success': True})
    return render(request, 'admin_hero_add.html')

def admin_hero_edit(request, id):
    image_obj = get_object_or_404(HeroImage, id=id)
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_obj.image = request.FILES['image']
        image_obj.title = request.POST.get('title')
        image_obj.subtitle = request.POST.get('subtitle')
        image_obj.save()
        return render(request, 'admin_hero_edit.html', {'image': image_obj, 'success': True})
    return render(request, 'admin_hero_edit.html', {'image': image_obj})

def admin_hero_delete(request, id):
    image_obj = get_object_or_404(HeroImage, id=id)
    image_obj.delete()
    return render(request, 'admin_hero_list.html', {'images': HeroImage.objects.all(), 'deleted': True})
def admin_gallery_list(request):
    images = GalleryImage.objects.all()
    return render(request, 'admin_gallery_list.html', {'images': images})

def admin_gallery_add(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        description = request.POST.get('description')
        if image:
            GalleryImage.objects.create(image=image, description=description)
            return render(request, 'admin_gallery_add.html', {'success': True})
    return render(request, 'admin_gallery_add.html')

def admin_gallery_edit(request, id):
    image_obj = get_object_or_404(GalleryImage, id=id)
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_obj.image = request.FILES['image']
        image_obj.description = request.POST.get('description')
        image_obj.save()
        return render(request, 'admin_gallery_edit.html', {'image': image_obj, 'success': True})
    return render(request, 'admin_gallery_edit.html', {'image': image_obj})

def admin_gallery_delete(request, id):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    try:
        image_obj = GalleryImage.objects.get(id=id)
        image_obj.delete()
        return HttpResponseRedirect(reverse('admin_gallery_list') + '?deleted=1')
    except GalleryImage.DoesNotExist:
        return HttpResponseRedirect(reverse('admin_gallery_list') + '?notfound=1')
def load_admin_app(request):
    return HttpResponse("Admin App Loaded Successfully")

def register(request):
    if request.method == 'POST':
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        image = request.FILES.get('photo')
        is_team = False
        if email == "sandra@bjsm.co.in":
            is_team = True
        user = userdetails(name=name, email=email, phone=phone, password=password, image=image, is_team=is_team)
        user.save()
        return render(request, 'register.html', {'success': True})
    return render(request, 'register.html')

def user_view(request):
    users = userdetails.objects.all()
    return render(request, 'user_view.html', {'users': users})

def user_delete(request, id):
    from django.http import HttpResponseNotFound, HttpResponseRedirect
    from django.urls import reverse
    try:
        user = userdetails.objects.get(id=id)
        user.delete()
    except userdetails.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('user_view'))

def user_update(request, id):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    user = userdetails.objects.get(id=id)
    if request.method == 'POST':
        user.name = request.POST.get('fullname')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.password = request.POST.get('password')
        if 'photo' in request.FILES:
            user.image = request.FILES['photo']
        user.save()
        return HttpResponseRedirect(reverse('user_view'))
    return render(request, 'user_update.html', {'user': user})

def admin_dashboard(request):
    from team_app.models import Order
    from hotel.models import Reservation
    from .models import maincategory, Category, SubCategory, SalesRevenue, Expense
    from django.db import models
    from django.utils import timezone
    from datetime import timedelta
    today = timezone.now().date()
    # Counts for boxes
    maincat_count = maincategory.objects.count()
    cat_count = Category.objects.count()
    subcat_count = SubCategory.objects.count()
    # Order/reservation counts
    pending_count = Order.objects.filter(status='Pending').count()
    preparing_count = Order.objects.filter(status='Preparing').count()
    delivered_count = Order.objects.filter(status='Delivered').count()
    new_reservation_count = Reservation.objects.filter(is_new=True).count()
    # Filter type
    filter_type = request.GET.get('filter', 'weekly')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    # Revenue/expense data for line graph (daily)
    import datetime
    if start_date and end_date:
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        filter_type = 'custom'
    elif filter_type == 'weekly':
        start = today - timedelta(days=6)
        end = today
    elif filter_type == 'monthly':
        start = today.replace(day=1)
        end = today
    elif filter_type == '3months':
        start = today - timedelta(days=90)
        end = today
    elif filter_type == '6months':
        start = today - timedelta(days=180)
        end = today
    else:
        start = today - timedelta(days=6)
        end = today
        filter_type = 'weekly'
    # Prepare daily labels and values
    num_days = (end - start).days + 1
    labels = [(start + timedelta(days=i)).strftime('%d-%b') for i in range(num_days)]
    revenue_data = []
    expense_data = []
    for i in range(num_days):
        day = start + timedelta(days=i)
        rev = SalesRevenue.objects.filter(delivered_at__date=day).aggregate(total=models.Sum('total'))['total'] or 0
        exp = Expense.objects.filter(date=day).aggregate(total=models.Sum('amount'))['total'] or 0
        revenue_data.append(rev)
        expense_data.append(exp)
    total_revenue = sum(revenue_data)
    total_expense = sum(expense_data)
    # Online order revenue for graph
    online_order_revenue_data = []
    from hotel.models import AcceptedOrder
    for i in range(num_days):
        day = start + timedelta(days=i)
        online_rev = AcceptedOrder.objects.filter(order_time__date=day).aggregate(total=models.Sum('total_price'))['total'] or 0
        online_order_revenue_data.append(online_rev)
    return render(request, 'admin_dashboard.html', {
        'maincat_count': maincat_count,
        'cat_count': cat_count,
        'subcat_count': subcat_count,
        'pending_count': pending_count,
        'preparing_count': preparing_count,
        'delivered_count': delivered_count,
        'new_reservation_count': new_reservation_count,
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'filter_type': filter_type,
        'start_date': start_date,
        'end_date': end_date,
        'today': today,
        'labels': labels,
        'revenue_data': revenue_data,
        'expense_data': expense_data,
        'online_order_revenue_data': online_order_revenue_data,
    })

def main_category(request):
    success = False
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            maincategory.objects.create(name=category_name)
            success = True
    return render(request, 'main_category.html', {'success': success})

def maincat_view(request):
    categories = maincategory.objects.all()
    return render(request, 'maincat_view.html', {'main_categories': categories})

def maincat_delete(request, id):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    try:
        category = maincategory.objects.get(id=id)
        category.delete()
    except maincategory.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('maincat_view'))


def category_view(request):
    from .models import maincategory, Category
    main_categories = maincategory.objects.all()
    success = False
    if request.method == 'POST':
        main_category_id = request.POST.get('main_category')
        category_name = request.POST.get('category_name')
        category_image = request.FILES.get('category_image')
        category_price = request.POST.get('category_price')
        if main_category_id and category_name:
            main_cat = maincategory.objects.get(id=main_category_id)
            cat_obj = Category(main_category=main_cat, name=category_name)
            if category_image:
                cat_obj.image = category_image
            if category_price:
                cat_obj.price = category_price
            cat_obj.save()
            success = True
    return render(request, 'category_view.html', {'main_categories': main_categories, 'success': success})

def cat_view(request):
    from .models import Category
    categories = Category.objects.select_related('main_category').all()
    return render(request, 'cat_view.html', {'categories': categories})

def cat_delete(request, id):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    from .models import Category
    try:
        category = Category.objects.get(id=id)
        category.delete()
    except Category.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('cat_view'))

def subcategory_view(request):
    from .models import maincategory, Category, SubCategory
    main_categories = maincategory.objects.all()
    categories = Category.objects.all()
    success = False
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    if request.method == 'POST':
        category_id = request.POST.get('category')
        item_name = request.POST.get('subcategory_name')
        item_image = request.FILES.get('subcategory_image')
        item_price = request.POST.get('subcategory_price')
        offer_price = request.POST.get('offer_price')
        description = request.POST.get('description')
        if category_id and item_name and item_price:
            cat = Category.objects.get(id=category_id)
            subcat = SubCategory(
                category=cat,
                name=item_name,
                price=item_price,
                offer_price=offer_price if offer_price else None,
                description=description if description else None
            )
            if item_image:
                subcat.image = item_image
            subcat.save()
            return HttpResponseRedirect(reverse('subcat_view'))
    return render(request, 'subcategory.html', {'main_categories': main_categories, 'categories': categories})

def subcat_view(request):
    from .models import SubCategory
    subcategories = SubCategory.objects.select_related('category__main_category').all()
    return render(request, 'subcat_view.html', {'subcategories': subcategories})
    # Placeholder view for subcat_view
    return render(request, 'subcat_view.html')

def subcat_delete(request, id):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    from .models import SubCategory
    try:
        subcat = SubCategory.objects.get(id=id)
        subcat.delete()
    except SubCategory.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('subcat_view'))

def subcat_update(request, id):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    from .models import SubCategory, Category
    from .models import maincategory
    subcat = SubCategory.objects.get(id=id)
    main_categories = maincategory.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        subcat.name = request.POST.get('subcategory_name')
        subcat.price = request.POST.get('subcategory_price')
        subcat.offer_price = request.POST.get('offer_price') if hasattr(subcat, 'offer_price') else None
        category_id = request.POST.get('category')
        if category_id:
            subcat.category = Category.objects.get(id=category_id)
        if 'subcategory_image' in request.FILES:
            subcat.image = request.FILES['subcategory_image']
        subcat.save()
        return HttpResponseRedirect(reverse('subcat_view'))
    return render(request, 'subcat_update.html', {'subcat': subcat, 'main_categories': main_categories, 'categories': categories})

def toggle_subcat_availability(request, id):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    from .models import SubCategory
    if request.method == 'POST':
        subcat = SubCategory.objects.get(id=id)
        subcat.is_available = not subcat.is_available
        subcat.save()
    return HttpResponseRedirect(reverse('subcat_view'))

def get_categories_by_main(request):
    from django.http import JsonResponse
    main_category_id = request.GET.get('main_category_id')
    if main_category_id:
        categories = Category.objects.filter(maincategory_id=main_category_id)
        data = [{'id': cat.id, 'name': cat.name} for cat in categories]
    else:
        data = []
    return JsonResponse({'categories': data})

def reservation_list(request):
    from hotel.models import Reservation
    reservations = Reservation.objects.all().order_by('-date', '-time')
    # Mark all new reservations as seen
    Reservation.objects.filter(is_new=True).update(is_new=False)
    return render(request, 'reservation_list.html', {'reservations': reservations})

def reservation_delete(request, id):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    try:
        from hotel.models import Reservation
        reservation = Reservation.objects.get(id=id)
        reservation.delete()
    except Exception:
        pass
    return HttpResponseRedirect(reverse('reservation_list'))

def chef_register(request):
    from .models import chef
    success = False
    error = None
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        image = request.FILES.get('image')
        specialty = request.POST.get('specialty')
        if password != confirm_password:
            error = "Passwords do not match."
        elif chef.objects.filter(email=email).exists():
            error = "Chef with this email already exists."
        else:
            chef_obj = chef(name=name, email=email, phone=phone, password=password, image=image, specialty=specialty)
            chef_obj.save()
            success = True
    return render(request, 'chef_register.html', {'success': success, 'error': error})

def our_chef(request):
    from .models import chef
    chefs = chef.objects.all()
    return render(request, 'our_chef.html', {'chefs': chefs})

def chef_delete(request, id):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    try:
        from .models import chef
        chef_obj = chef.objects.get(id=id)
        chef_obj.delete()
    except Exception:
        pass
    return HttpResponseRedirect(reverse('our_chef'))

def chef_update(request, id):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    from .models import chef
    chef_obj = chef.objects.get(id=id)
    success = False
    error = None
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        image = request.FILES.get('image')
        if password and password != confirm_password:
            error = "Passwords do not match."
        else:
            chef_obj.name = name
            chef_obj.email = email
            chef_obj.phone = phone
            if password:
                chef_obj.password = password
            if image:
                chef_obj.image = image
            chef_obj.save()
            success = True
            return HttpResponseRedirect(reverse('our_chef'))
    return render(request, 'chef_update.html', {'chef': chef_obj, 'success': success, 'error': error})
    return render(request, 'chef_update.html', {'chef': chef})

def sales_revenue(request):
    from datetime import timedelta
    from django.utils import timezone
    today = timezone.now().date()
    # Delete sales revenue older than 2 years
    two_years_ago = today.replace(year=today.year-2)
    SalesRevenue.objects.filter(delivered_at__date__lt=two_years_ago).delete()

    # Filtering logic (same as expense_list)
    filter_type = request.GET.get('filter', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    orders = SalesRevenue.objects.all()
    if start_date and end_date:
        orders = orders.filter(delivered_at__date__gte=start_date, delivered_at__date__lte=end_date)
        filter_type = 'custom'
    elif filter_type == 'daily':
        orders = orders.filter(delivered_at__date=today)
    elif filter_type == 'weekly':
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        orders = orders.filter(delivered_at__date__gte=week_start, delivered_at__date__lte=week_end)
    elif filter_type == 'monthly':
        orders = orders.filter(delivered_at__year=today.year, delivered_at__month=today.month)
    elif filter_type == '3months':
        three_months_ago = today - timedelta(days=90)
        orders = orders.filter(delivered_at__date__gte=three_months_ago)
    elif filter_type == '6months':
        six_months_ago = today - timedelta(days=180)
        orders = orders.filter(delivered_at__date__gte=six_months_ago)
    # else: all
    orders = orders.order_by('-delivered_at')
    total_amount = sum(order.amount for order in orders)
    total_gst = sum(order.gst for order in orders)
    total_total = sum(order.total for order in orders)
    return render(request, 'sales_revenue.html', {
        'orders': orders,
        'total_amount': total_amount,
        'total_gst': total_gst,
        'total_total': total_total,
        'filter_type': filter_type,
        'start_date': start_date,
        'end_date': end_date,
        'today': today,
    })

def add_expense(request):
    from .models import Expense
    from django.utils import timezone
    today = timezone.now().date()
    success = False
    error = None
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        date = request.POST.get('date') or today
        payment_method = request.POST.get('payment_method')
        notes = request.POST.get('notes')
        amount = request.POST.get('amount')
        bill = request.FILES.get('bill')
        # Validation (all except notes and bill required)
        if not (name and category and date and payment_method and amount):
            error = "All fields except notes and bill are required."
        else:
            Expense.objects.create(
                name=name,
                category=category,
                date=date,
                payment_method=payment_method,
                notes=notes,
                amount=amount,
                bill=bill
            )
            success = True
    return render(request, 'add_expense.html', {'today': today, 'success': success, 'error': error})

def expense_list(request):
    from .models import Expense
    from datetime import timedelta
    from django.utils import timezone
    import calendar
    filter_type = request.GET.get('filter', 'all')
    today = timezone.now().date()
    # Delete expenses older than 2 years
    two_years_ago = today.replace(year=today.year-2)
    Expense.objects.filter(date__lt=two_years_ago).delete()
    # Custom date range search
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expenses = Expense.objects.all()
    if start_date and end_date:
        expenses = expenses.filter(date__gte=start_date, date__lte=end_date)
        filter_type = 'custom'
    elif filter_type == 'daily':
        expenses = expenses.filter(date=today)
    elif filter_type == 'weekly':
        start = today - timedelta(days=7)
        expenses = expenses.filter(date__gte=start, date__lte=today)
    elif filter_type == 'monthly':
        start = today.replace(day=1)
        expenses = expenses.filter(date__gte=start, date__lte=today)
    elif filter_type == '3months':
        start = today - timedelta(days=90)
        expenses = expenses.filter(date__gte=start, date__lte=today)
    elif filter_type == '6months':
        start = today - timedelta(days=180)
        expenses = expenses.filter(date__gte=start, date__lte=today)
    expenses = expenses.order_by('-date')
    total_amount = sum(exp.amount for exp in expenses)
    return render(request, 'expense_list.html', {
        'expenses': expenses,
        'total_amount': total_amount,
        'filter_type': filter_type,
        'start_date': start_date,
        'end_date': end_date
    })

def expense_delete(request, id):
    from .models import Expense
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('expense_list')

def expense_update(request, id):
    from .models import Expense
    from django.utils import timezone
    expense = get_object_or_404(Expense, id=id)
    today = timezone.now().date()
    success = False
    error = None
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        date = request.POST.get('date') or today
        payment_method = request.POST.get('payment_method')
        notes = request.POST.get('notes')
        amount = request.POST.get('amount')
        bill = request.FILES.get('bill')
        if not (name and category and date and payment_method and amount):
            error = "All fields except notes and bill are required."
        else:
            expense.name = name
            expense.category = category
            expense.date = date
            expense.payment_method = payment_method
            expense.notes = notes
            expense.amount = amount
            if bill:
                expense.bill = bill
            expense.save()
            success = True
    return render(request, 'expense_update.html', {'expense': expense, 'today': today, 'success': success, 'error': error, 'update': True})