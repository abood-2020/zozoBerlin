# Generated by Django 4.1.4 on 2024-09-10 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0011_apartment_promotional_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='location',
        ),
        migrations.AddField(
            model_name='apartment',
            name='location_url',
            field=models.URLField(blank=True, help_text='Location of the apartment', null=True, verbose_name='Location'),
        ),
    ]
