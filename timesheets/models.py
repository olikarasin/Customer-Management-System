from django.db import models
from customers.models import Customer
from decimal import Decimal
from django.utils.timezone import make_aware
from datetime import datetime, time

class Timesheet(models.Model):
    customer = models.ForeignKey(Customer, related_name='timesheets', on_delete=models.CASCADE)
    timesheet_id = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    technician_level = models.IntegerField(choices=((1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3')))
    special_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional special rate
    total_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    file = models.FileField(upload_to='timesheets/')
    notes = models.TextField(blank=True, null=True)

    def calculate_hours(self, start, end):
        """ Calculate hours between two datetime objects. """
        total_seconds = (end - start).total_seconds()
        return total_seconds / 3600

    def save(self, *args, **kwargs):
        """ Override the save method to calculate charges based on the customer's technician rates. """
        rate_dict = {
            1: (self.customer.tech1_regular_hours, self.customer.tech1_time_and_a_half_hours, self.customer.tech1_double_time_hours),
            2: (self.customer.tech2_regular_hours, self.customer.tech2_time_and_a_half_hours, self.customer.tech2_double_time_hours),
            3: (self.customer.tech3_regular_hours, self.customer.tech3_time_and_a_half_hours, self.customer.tech3_double_time_hours),
        }
        regular_rate, time_and_a_half_rate, double_time_rate = rate_dict[self.technician_level]

        # Times for calculations
        day_start = time(8, 0)  # 8 AM
        evening_start = time(17, 0)  # 5 PM
        night_end = time(8, 0)  # Next day 8 AM

        # Convert time_in and time_out to datetime objects
        datetime_in = make_aware(datetime.combine(self.date, self.time_in))
        datetime_out = make_aware(datetime.combine(self.date, self.time_out))

        total_charge = Decimal(0)

        # Calculate charges for regular, time and a half, and double time
        current_time = datetime_in
        while current_time < datetime_out:
            next_time_boundary = None
            current_rate = None

            if current_time.time() < day_start:
                # Current time is in double time (night time)
                next_time_boundary = make_aware(datetime.combine(self.date, day_start))
                current_rate = double_time_rate
            elif current_time.time() < evening_start:
                # Current time is in regular time
                next_time_boundary = make_aware(datetime.combine(self.date, evening_start))
                current_rate = regular_rate
            else:
                # Current time is in time and a half (evening time)
                next_time_boundary = make_aware(datetime.combine(self.date + timedelta(days=1), night_end))
                current_rate = time_and_a_half_rate

            if datetime_out < next_time_boundary:
                next_time_boundary = datetime_out

            hours = self.calculate_hours(current_time, next_time_boundary)
            total_charge += Decimal(hours) * current_rate
            current_time = next_time_boundary

        self.total_charge = total_charge
        super(Timesheet, self).save(*args, **kwargs)

    def __str__(self):
        return f"Timesheet {self.timesheet_id} for {self.customer.name}"
