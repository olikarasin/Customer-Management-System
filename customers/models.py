from django.db import models
from django.contrib.auth.models import User

class Technician(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class EmailReference(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

class Customer(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE, default=1)  # Replace 1 with the actual default user ID
    name = models.CharField(max_length=255)
    has_contract = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    transport_hours = models.IntegerField(default=0)
    transport_minutes = models.IntegerField(default=0)
    hide_transport_charges = models.BooleanField(default=False)
    hours_remaining = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive')
    emails = models.ManyToManyField(EmailReference, blank=True)

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
        if self.hours_remaining == 0:
            self.status = 'Inactive'
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Contract(models.Model):
    customer = models.ForeignKey(Customer, related_name='contracts', on_delete=models.CASCADE)
    date = models.CharField(max_length=8)  # Store date as a char field for YYYYMMDD format
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    manual_charge_hours = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    manual_charge_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.manual_charge_hours and self.manual_charge_amount:
            self.hours = self.manual_charge_hours
            self.amount = self.manual_charge_amount
        else:
            self.hours = self.amount / self.rate
        
        super(Contract, self).save(*args, **kwargs)

        if self.approved:
            self.customer.hours_remaining += self.hours
            self.customer.save()

    def __str__(self):
        return f"Contract {self.invoice_number} for {self.customer.name}"

class Credential(models.Model):
    customer = models.ForeignKey(Customer, related_name='credentials', on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Plaintext password

    def __str__(self):
        return self.username

class Timesheet(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_timesheets', on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, related_name='technician_timesheets', on_delete=models.CASCADE)
    date = models.DateField()
    regular_hours = models.DecimalField(max_digits=5, decimal_places=2)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2)
    doubletime_hours = models.DecimalField(max_digits=5, decimal_places=2)
    approved = models.BooleanField(default=False)  # Add this line if timesheets need approval

    def __str__(self):
        return f"Timesheet for {self.customer.name} on {self.date}"
