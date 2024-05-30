# Generated by Django 4.2.13 on 2024-05-30 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_technician'),
        ('timesheets', '0005_timesheet_technician_name_timesheet_total_time_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='technician_name',
        ),
        migrations.RemoveField(
            model_name='timesheet',
            name='total_time_used',
        ),
        migrations.AddField(
            model_name='timesheet',
            name='technician',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.technician'),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='timesheet_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
