from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Technician(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class EmailReference(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

class Customer(models.Model):
    name = models.CharField(max_length=255)
    has_contract = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    transport_hours = models.IntegerField(default=0)
    transport_minutes = models.IntegerField(default=0)
    hide_transport_charges = models.BooleanField(default=False)
    hours_remaining = models.IntegerField(default=0)  # Field for hours remaining
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive')  # Field for status
    emails = models.ManyToManyField(EmailReference, blank=True)

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

    def save(self, *args, **kwargs):
        # Automatically set status to 'Inactive' if hours_remaining is 0
        if self.hours_remaining == 0:
            self.status = 'Inactive'
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Contract(models.Model):
    customer = models.ForeignKey(Customer, related_name='contracts', on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Default value added
    paid = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.hours = self.amount / self.rate
        super(Contract, self).save(*args, **kwargs)

    def __str__(self):
        return f"Contract {self.invoice_number} for {self.customer.name}"

class Credential(models.Model):
    customer = models.ForeignKey(Customer, related_name='credentials', on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f'{self.customer.name} - {self.username}'
