from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    has_contract = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    transport_hours = models.IntegerField(default=0)
    transport_minutes = models.IntegerField(default=0)
    hide_transport_charges = models.BooleanField(default=False)

    # Technician levels 
    tech1_regular_hours = models.IntegerField(default=0)
    tech1_time_and_a_half_hours = models.IntegerField(default=0)
    tech1_double_time_hours = models.IntegerField(default=0)
    tech2_regular_hours = models.IntegerField(default=0)
    tech2_time_and_a_half_hours = models.IntegerField(default=0)
    tech2_double_time_hours = models.IntegerField(default=0)
    tech3_regular_hours = models.IntegerField(default=0)
    tech3_time_and_a_half_hours = models.IntegerField(default=0)
    tech3_double_time_hours = models.IntegerField(default=0)

    def __str__(self):
        return self.name
