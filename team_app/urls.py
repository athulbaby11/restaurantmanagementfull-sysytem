
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
    path('load_team_app/', views.load_team_app, name='load_team_app'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('team_dashboard/', views.team_dashboard, name='team_dashboard'),
    path('team_dashboard.html', views.team_dashboard),
    path('order_view/', views.team_order_menu, name='team_order_menu'),
    path('order_view/<int:table_number>/', views.order_view, name='order_view'),
    path('add_to_team_cart/', views.add_to_team_cart, name='add_to_team_cart'),
    path('team_cart/', views.team_cart, name='team_cart'),
    path('remove_team_cart_item/', views.remove_team_cart_item, name='remove_team_cart_item'),
    path('update_team_cart_item/', views.update_team_cart_item, name='update_team_cart_item'),
    path('place_order/', views.place_order, name='place_order'),
    path('delete_order/', views.delete_order, name='delete_order'),
    path('unavailable_items/', views.today_unavailable_items, name='unavailable_items'),

]
