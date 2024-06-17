from django.contrib import admin
from .models import Customer, Technician, EmailReference  # Import EmailReference model

admin.site.register(Customer)
admin.site.register(Technician)
admin.site.register(EmailReference)  # Register EmailReference model
