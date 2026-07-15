from django.db import models
# Model to store delivered order details by chef
class ChefDeliveredOrder(models.Model):
	order_id = models.IntegerField()
	table_number = models.CharField(max_length=50)
	placed_at = models.DateTimeField()
	amount = models.FloatField()
	gst = models.FloatField()
	total = models.FloatField()
	delivered_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Delivered Order {self.order_id} (Table {self.table_number})"
from django.db import models
from team_app.models import Order
from team_app.models import OrderItem
from hotel.models import Reservation

# Create your models here.


    
