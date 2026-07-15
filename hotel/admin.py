from django.contrib import admin
from .models import Reservation, GalleryImage, HeroImage, News, UserOrder, AcceptedOrder, AcceptedOrderItem, UserOrderItem

admin.site.register(Reservation)
admin.site.register(GalleryImage)
admin.site.register(HeroImage)
admin.site.register(News)
admin.site.register(UserOrder)
admin.site.register(AcceptedOrder)
admin.site.register(AcceptedOrderItem)
admin.site.register(UserOrderItem)
