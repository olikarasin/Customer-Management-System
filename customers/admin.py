# customers/admin.py
from django.contrib import admin
from .models import Customer, Technician  # Import Technician model

admin.site.register(Customer)
admin.site.register(Technician)  # Register Technician model
