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
from django.urls import path, include
from django.views.generic.base import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('book_table/',views.book_table,name='book_table'),
    path('add_to_user_cart/', views.add_to_user_cart, name='add_to_user_cart'),
    path('user_cart/', views.user_cart, name='user_cart'),
    path('update_user_cart/', views.update_user_cart, name='update_user_cart'),
    path('remove_user_cart/', views.remove_user_cart, name='remove_user_cart'),
    path('user_checkout/', views.user_checkout, name='user_checkout'),
    path('menu/', views.menu_page, name='menu_page'),
    path('set_currency/', views.set_currency, name='set_currency'),
    path('about/', views.about_page, name='about_page'),
    path('about.html', views.about_page),
    path('order.html', RedirectView.as_view(pattern_name='menu_page', permanent=False)),
    path('', include('admin_app.urls')),
    path('', include('team_app.urls')),
    path('', include('user_app.urls')),
    path('', include('Chef_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
