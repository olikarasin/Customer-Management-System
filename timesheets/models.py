# timesheets/models.py
from django.db import models
from customers.models import Customer, Technician
from decimal import Decimal
from django.utils.timezone import make_aware
from datetime import datetime, time, timedelta

class Timesheet(models.Model):
    customer = models.ForeignKey(Customer, related_name='timesheets', on_delete=models.CASCADE)
    timesheet_id = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    technician_level = models.IntegerField(choices=((1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3')))
    special_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    file = models.FileField(upload_to='timesheets/')
    notes = models.TextField(blank=True, null=True)
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, default=None)  # Added default=None

    def save(self, *args, **kwargs):
        rate_dict = {
            1: (self.customer.tech1_regular_hours, self.customer.tech1_time_and_a_half_hours, self.customer.tech1_double_time_hours),
            2: (self.customer.tech2_regular_hours, self.customer.tech2_time_and_a_half_hours, self.customer.tech2_double_time_hours),
            3: (self.customer.tech3_regular_hours, self.customer.tech3_time_and_a_half_hours, self.customer.tech3_double_time_hours),
        }
        regular_rate, time_and_a_half_rate, double_time_rate = rate_dict[self.technician_level]

        if self.special_rate:
            self.total_charge = self.special_rate
        else:
            self.total_charge = calculate_total_charge(self, regular_rate, time_and_a_half_rate, double_time_rate)
        
        super(Timesheet, self).save(*args, **kwargs)

    def __str__(self):
        return f"Timesheet {self.timesheet_id} for {self.customer.name}"

def calculate_total_charge(timesheet, regular_rate, time_and_a_half_rate, double_time_rate):
    day_start = time(8, 0)
    evening_start = time(17, 0)
    night_end = time(8, 0)

    datetime_in = make_aware(datetime.combine(timesheet.date, timesheet.time_in))
    datetime_out = make_aware(datetime.combine(timesheet.date, timesheet.time_out))

    total_charge = Decimal(0)
    current_time = datetime_in

    while current_time < datetime_out:
        if current_time.time() < day_start:
            next_time_boundary = make_aware(datetime.combine(current_time.date(), day_start))
            current_rate = double_time_rate
        elif current_time.time() < evening_start:
            next_time_boundary = make_aware(datetime.combine(current_time.date(), evening_start))
            current_rate = regular_rate
        else:
            next_time_boundary = make_aware(datetime.combine(current_time.date() + timedelta(days=1), night_end))
            current_rate = time_and_a_half_rate

        if datetime_out < next_time_boundary:
            next_time_boundary = datetime_out

        hours = (next_time_boundary - current_time).total_seconds() / 3600
        rounded_hours = (Decimal(hours * 4).quantize(Decimal('1.0')) / 4).quantize(Decimal('0.25'), rounding='ROUND_UP')
        total_charge += rounded_hours * Decimal(current_rate)
        current_time = next_time_boundary

    return total_charge
