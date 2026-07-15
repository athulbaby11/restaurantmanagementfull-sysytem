from django.db import models

# Gallery image model
class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery_images/')
    caption = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.caption or str(self.image)

# Hero image model
class HeroImage(models.Model):
    image = models.ImageField(upload_to='hero_images/')
    headline = models.CharField(max_length=200)
    subheadline = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.headline

# News model
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title
from django.db import models

class UserOrder(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    zipcode = models.CharField(max_length=20, default="")
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20)
    order_time = models.DateTimeField(auto_now_add=True)
    delivered_place = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")


class AcceptedOrder(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    zipcode = models.CharField(max_length=20, default="")
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20)
    order_time = models.DateTimeField()
    delivered_place = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class AcceptedOrderItem(models.Model):
    accepted_order = models.ForeignKey(AcceptedOrder, related_name='items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class UserOrderItem(models.Model):
    user_order = models.ForeignKey(UserOrder, related_name='items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# Create your models here.

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    people = models.IntegerField()
    message = models.TextField(blank=True)
    is_new = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"
