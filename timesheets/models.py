# timesheets/models.py
from decimal import Decimal, ROUND_UP
from django.utils.timezone import make_aware
from datetime import datetime, time, timedelta
from django.db import models
from customers.models import Customer, Technician
import holidays  # Ensure correct import

def calculate_total_charge(timesheet, regular_rate, time_and_a_half_rate, double_time_rate):
    day_start = time(8, 0)  # 8 AM
    evening_start = time(17, 0)  # 5 PM
    night_end = time(8, 0)  # Next day 8 AM

    datetime_in = make_aware(datetime.combine(timesheet.date, timesheet.time_in))
    datetime_out = make_aware(datetime.combine(timesheet.date, timesheet.time_out))

    total_charge = Decimal(0)
    total_time_used = Decimal(0)
    current_time = datetime_in

    # Check if the date is a holiday in Quebec
    quebec_holidays = holidays.CA(prov='QC')
    is_holiday = timesheet.date in quebec_holidays

    while current_time < datetime_out:
        if current_time.time() < day_start:
            next_time_boundary = make_aware(datetime.combine(current_time.date(), day_start))
            current_rate = double_time_rate
            time_multiplier = 2
        elif current_time.time() < evening_start:
            next_time_boundary = make_aware(datetime.combine(current_time.date(), evening_start))
            current_rate = regular_rate
            time_multiplier = 1
        else:
            next_time_boundary = make_aware(datetime.combine(current_time.date() + timedelta(days=1), night_end))
            current_rate = time_and_a_half_rate
            time_multiplier = 1.5

        if datetime_out < next_time_boundary:
            next_time_boundary = datetime_out

        duration_minutes = (next_time_boundary - current_time).total_seconds() / 60
        rounded_minutes = (duration_minutes + 14) // 15 * 15
        rounded_hours = Decimal(rounded_minutes) / 60

        if timesheet.special_rate:
            current_rate = timesheet.special_rate
            if is_holiday:
                if current_time.time() < day_start:
                    time_multiplier = 4
                elif current_time.time() < evening_start:
                    time_multiplier = 2
                else:
                    time_multiplier = 3
            total_charge += rounded_hours * Decimal(current_rate) * Decimal(time_multiplier)
        else:
            if is_holiday:
                if current_time.time() < day_start:
                    current_rate = double_time_rate * 2
                    time_multiplier = 4
                elif current_time.time() < evening_start:
                    current_rate = regular_rate * 2
                    time_multiplier = 2
                else:
                    current_rate = time_and_a_half_rate * 2
                    time_multiplier = 3
            total_charge += rounded_hours * Decimal(current_rate)
        
        total_time_used += rounded_hours * Decimal(time_multiplier)

        current_time = next_time_boundary

    # Subtract the pause duration
    pause_hours, pause_minutes = map(int, timesheet.pause.split('h'))
    pause_duration = Decimal(pause_hours + pause_minutes / 60)
    total_charge -= regular_rate * pause_duration  # Subtract pause duration charge
    total_time_used -= pause_duration

    return total_charge, total_time_used

class Timesheet(models.Model):
    customer = models.ForeignKey(Customer, related_name='timesheets', on_delete=models.CASCADE)
    timesheet_id = models.CharField(max_length=100)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    technician_level = models.IntegerField(choices=((1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3')))
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    special_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_time_used = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pause = models.CharField(max_length=10, default='0h0')  # Add pause field
    file = models.FileField(upload_to='timesheets/', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)  # New field to track approval

    def save(self, *args, **kwargs):
        rate_dict = {
            1: (self.customer.tech1_regular_hours, self.customer.tech1_time_and_a_half_hours, self.customer.tech1_double_time_hours),
            2: (self.customer.tech2_regular_hours, self.customer.tech2_time_and_a_half_hours, self.customer.tech2_double_time_hours),
            3: (self.customer.tech3_regular_hours, self.customer.tech3_time_and_a_half_hours, self.customer.tech3_double_time_hours),
        }
        regular_rate, time_and_a_half_rate, double_time_rate = rate_dict[self.technician_level]

        if self.special_rate:
            total_charge, total_time_used = calculate_total_charge(self, self.special_rate, self.special_rate * Decimal(1.5), self.special_rate * Decimal(2))
        else:
            total_charge, total_time_used = calculate_total_charge(self, regular_rate, time_and_a_half_rate, double_time_rate)

        self.total_charge = total_charge
        self.total_time_used = total_time_used

        # Adjust customer's hours only if the timesheet is approved
        if self.approved:
            self.customer.hours_remaining -= self.total_time_used
            self.customer.hours_remaining = (Decimal(self.customer.hours_remaining * 4).quantize(Decimal('1.0')) / 4).quantize(Decimal('0.25'), rounding=ROUND_UP)
            self.customer.save()

        super(Timesheet, self).save(*args, **kwargs)

    def __str__(self):
        return f"Timesheet {self.timesheet_id} for {self.customer.name}"
