from django.db import models
from customers.models import Customer
from decimal import Decimal
from datetime import time, datetime, timedelta

class Timesheet(models.Model):
    LEVEL_CHOICES = (
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
    )

    customer = models.ForeignKey(Customer, related_name='timesheets', on_delete=models.CASCADE)
    timesheet_id = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    technician_level = models.IntegerField(choices=LEVEL_CHOICES)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    file = models.FileField(upload_to='timesheets/')
    notes = models.TextField(blank=True, null=True)

    def calculate_hours(self, start, end, rate):
        """ Calculate hourly rates based on the given time range and rate """
        total_hours = (end - start).seconds / 3600
        return Decimal(total_hours) * rate

    def save(self, *args, **kwargs):
        # Define time blocks
        day_start = time(8, 0)  # 8 AM
        evening_start = time(17, 0)  # 5 PM
        night_start = time(0, 0)  # Midnight
        night_end = time(8, 0)  # 8 AM

        # Initialize total_charge
        self.total_charge = Decimal(0)

        # Calculate the total charge based on technician rates and time blocks
        rates = {
            'regular': Decimal(self.rate),
            'time_and_a_half': Decimal(self.rate) * Decimal(1.5),
            'double_time': Decimal(self.rate) * Decimal(2)
        }

        # Convert times to datetime objects for comparison
        datetime_in = datetime.combine(self.date, self.time_in)
        datetime_out = datetime.combine(self.date, self.time_out)

        # Handle wrapping around midnight
        if datetime_in > datetime_out:
            datetime_out += timedelta(days=1)

        # Process each segment
        current_time = datetime_in
        while current_time < datetime_out:
            next_time = None
            rate_key = 'regular'

            if day_start <= current_time.time() < evening_start:
                next_time = datetime.combine(current_time.date(), evening_start)
                rate_key = 'regular'
            elif evening_start <= current_time.time() < night_start:
                next_time = datetime.combine(current_time.date(), night_start)
                rate_key = 'time_and_a_half'
            else:  # Night time
                next_boundary = datetime.combine(current_time.date() + timedelta(days=1), day_start)
                next_time = min(next_boundary, datetime_out)
                rate_key = 'double_time'

            if next_time > datetime_out:
                next_time = datetime_out

            self.total_charge += self.calculate_hours(current_time, next_time, rates[rate_key])
            current_time = next_time

        super(Timesheet, self).save(*args, **kwargs)

    def __str__(self):
        return f"Timesheet {self.timesheet_id} for {self.customer.name}"
