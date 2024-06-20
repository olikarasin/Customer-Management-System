# Generated by Django 4.2.13 on 2024-06-20 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0011_contract_hours_alter_customer_hours_remaining'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credentials', to='customers.customer')),
            ],
        ),
    ]
