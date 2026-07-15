from django.db import models

# Category model
class Category(models.Model):
    main_category = models.ForeignKey('maincategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# SubCategory model
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='subcategory_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    offer_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    description = models.TextField(max_length=420, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    VAT_CHOICES = [
        ('include', 'VAT include'),
        ('vatl_include', 'VATL include'),
        ('not_include', 'Not include'),
    ]
    vat_status = models.CharField(max_length=20, choices=VAT_CHOICES, default='not_include')
    

    def __str__(self):
        return self.name

# Create your models here.

class userdetails(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user_images/')
    is_team = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class maincategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class chef(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to='chef_images/')
    specialty = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class SalesRevenue(models.Model):
    order_id = models.IntegerField()
    delivered_at = models.DateTimeField()
    amount = models.FloatField()
    gst = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return f"Order {self.order_id} - {self.total}"

class Expense(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    amount = models.FloatField()
    bill = models.FileField(upload_to='expense_bills/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"