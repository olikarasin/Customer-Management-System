# Generated by Django 4.2.13 on 2024-07-12 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0005_rename_user_customer_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='user_profile',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
