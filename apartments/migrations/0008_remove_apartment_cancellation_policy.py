# Generated by Django 4.1.4 on 2024-08-23 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0007_remove_apartment_features'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='cancellation_policy',
        ),
    ]
