"""
URL configuration for hotel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from . import views

urlpatterns = [
    path('admin_gallery/', views.admin_gallery_list, name='admin_gallery_list'),
    path('admin_gallery/add/', views.admin_gallery_add, name='admin_gallery_add'),
    path('admin_gallery/edit/<int:id>/', views.admin_gallery_edit, name='admin_gallery_edit'),
    path('admin_gallery/delete/<int:id>/', views.admin_gallery_delete, name='admin_gallery_delete'),
    path('admin_hero/', views.admin_hero_list, name='admin_hero_list'),
    path('admin_hero/add/', views.admin_hero_add, name='admin_hero_add'),
    path('admin_hero/edit/<int:id>/', views.admin_hero_edit, name='admin_hero_edit'),
    path('admin_hero/delete/<int:id>/', views.admin_hero_delete, name='admin_hero_delete'),
    path('admin_news/', views.admin_news_list, name='admin_news_list'),
    path('admin_news/add/', views.admin_news_add, name='admin_news_add'),
    path('admin_news/edit/<int:id>/', views.admin_news_edit, name='admin_news_edit'),
    path('admin_news/delete/<int:id>/', views.admin_news_delete, name='admin_news_delete'),
                path('all_approved_orders/', views.all_approved_orders, name='all_approved_orders'),
            path('admin_online_order_accept/<int:id>/', views.admin_online_order_accept, name='admin_online_order_accept'),
            path('admin_online_order_delete/<int:id>/', views.admin_online_order_delete, name='admin_online_order_delete'),
        path('admin_online_orders/', views.admin_online_orders, name='admin_online_orders'),
    path('load_admin_app/', views.load_admin_app, name='load_admin_app'),
    path('register/', views.register, name='register'),
    path('user_view/', views.user_view, name='user_view'),
    path('user_delete/<int:id>/', views.user_delete, name='user_delete'),
    path('user_update/<int:id>/', views.user_update, name='user_update'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('main_category/', views.main_category, name='main_category'),
    path('maincat_view/', views.maincat_view, name='maincat_view'),
    path('maincat_delete/<int:id>/', views.maincat_delete, name='maincat_delete'),
    path('category_view/', views.category_view, name='category_view'),
    path('cat_view/', views.cat_view, name='cat_view'),
    path('cat_delete/<int:id>/', views.cat_delete, name='cat_delete'),
    path('subcategory_view/', views.subcategory_view, name='subcategory_view'),
    path('get_categories_by_main/', views.get_categories_by_main, name='get_categories_by_main'),
    path('subcat_view/', views.subcat_view, name='subcat_view'),
    path('subcat_delete/<int:id>/', views.subcat_delete, name='subcat_delete'),
    path('subcat_update/<int:id>/', views.subcat_update, name='subcat_update'),
    path('toggle_subcat_availability/<int:id>/', views.toggle_subcat_availability, name='toggle_subcat_availability'),
    path('toggle_subcat_vat/<int:id>/', views.toggle_subcat_vat, name='toggle_subcat_vat'),
    path('reservation_list/', views.reservation_list, name='reservation_list'),
    path('reservation_delete/<int:id>/', views.reservation_delete, name='reservation_delete'),
    path('chef_register/', views.chef_register, name='chef_register'),
    path('our_chef/', views.our_chef, name='our_chef'),
    path('chef_delete/<int:id>/', views.chef_delete, name='chef_delete'),
    path('chef_update/<int:id>/', views.chef_update, name='chef_update'),
    path('sales_revenue/', views.sales_revenue, name='sales_revenue'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('expense_list/', views.expense_list, name='expense_list'),
    path('expense_delete/<int:id>/', views.expense_delete, name='expense_delete'),
    path('expense_update/<int:id>/', views.expense_update, name='expense_update'),
]
