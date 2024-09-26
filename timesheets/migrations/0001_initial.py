# Generated by Django 4.2.13 on 2024-09-26 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timesheet_id', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=10)),
                ('time_in', models.CharField(max_length=5)),
                ('time_out', models.CharField(max_length=5)),
                ('technician_level', models.IntegerField(choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3')])),
                ('special_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_charge', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_time_used', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('pause_hours', models.IntegerField(blank=True, null=True)),
                ('pause_minutes', models.IntegerField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='timesheets/')),
                ('notes', models.TextField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('display_notes_to_customer', models.BooleanField(default=False)),
                ('manual_charge_hours', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('manual_charge_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timesheets', to='customers.customer')),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.technician')),
            ],
        ),
    ]
