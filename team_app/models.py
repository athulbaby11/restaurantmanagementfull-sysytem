from django.db import models

class Order(models.Model):
    table_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    subtotal = models.FloatField(blank=True, null=True)
    gst = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    qty = models.PositiveIntegerField()
    price = models.FloatField()
    total = models.FloatField()

class DeliveredOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    table_number = models.CharField(max_length=10)
    subtotal = models.FloatField()
    gst = models.FloatField()
    totalamount = models.FloatField()
    delivered_at = models.DateTimeField(auto_now_add=True)