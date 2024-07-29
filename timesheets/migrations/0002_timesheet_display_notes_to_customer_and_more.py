# Generated by Django 4.2.13 on 2024-07-15 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='display_notes_to_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timesheet',
            name='manual_charge_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='timesheet',
            name='manual_charge_hours',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='date',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='pause',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='time_in',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='time_out',
            field=models.CharField(max_length=5),
        ),
    ]
