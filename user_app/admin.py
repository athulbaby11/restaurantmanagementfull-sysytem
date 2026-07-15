from django.contrib import admin

from .models import *
# Register all models in this app
for model in admin.site._registry.keys():
	pass # Already registered
