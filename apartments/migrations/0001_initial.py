# Generated by Django 4.1.4 on 2024-07-05 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the apatment (must be unique)', max_length=255, unique=1, verbose_name='Apartment Title')),
                ('description', models.TextField(help_text='Detailed Description of the apartment', verbose_name='Description')),
                ('location', models.CharField(help_text='Location of the apartment', max_length=255, verbose_name='Location')),
                ('price_per_night', models.DecimalField(decimal_places=2, help_text='Price per night in USD', max_digits=10, verbose_name='Price per Night')),
                ('max_guests', models.IntegerField(help_text='Maximum number of guests allowed', verbose_name='Max Guest')),
                ('num_bedrooms', models.IntegerField(help_text='Number of bedrooms in the apartment.', verbose_name='Number of Bedrooms')),
                ('features', models.JSONField(help_text='Json List of featurs and amenities', verbose_name='Features and Ameaities')),
                ('images', models.JSONField(help_text='Json list of Image URLs.', verbose_name='Images')),
                ('check_in_time', models.TimeField(help_text='Check-in time', verbose_name='Check-in Time')),
                ('check_out_time', models.TimeField(help_text='check-out time', verbose_name='Check-out Time')),
                ('house_rules', models.TextField(help_text='House rules for the apartment', verbose_name='House Rules')),
                ('cancellation_policy', models.TextField(help_text='Cancellation policy details.', verbose_name='Cancellation Policy')),
            ],
        ),
    ]
