from django.contrib import admin
from .models import userdetails, Category, SubCategory, maincategory, SalesRevenue, Expense

admin.site.register(userdetails)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(maincategory)
admin.site.register(SalesRevenue)
admin.site.register(Expense)
