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
    path('load_chef_app/', views.load_chef_app, name='load_chef_app'),
    path('chef_profile/', views.chef_profile, name='chef_profile'),
    path('chef_dashboard/', views.chef_dashboard, name='chef_dashboard'),
    path('cheforder_request/', views.cheforder_request, name='cheforder_request'),
    path('cheforder_accept/<int:id>/', views.cheforder_accept, name='cheforder_accept'),
    path('cheforder_deliver/<int:id>/', views.cheforder_deliver, name='cheforder_deliver'),
    path('cheforder_delete/<int:id>/', views.cheforder_delete, name='cheforder_delete'),
    path('cheforder_delivered/<int:id>/', views.cheforder_delivered, name='cheforder_delivered'),
    path('chef_completed_orders/', views.chef_completed_orders, name='chef_completed_orders'),
    path('chef_online_orders/', views.chef_online_orders, name='chef_online_orders'),
    path('chef_order_delivered/<int:id>/', views.chef_order_delivered, name='chef_order_delivered'),
    path('online_order_revenue/', views.chef_online_order_revenue, name='online_order_revenue'),
]
