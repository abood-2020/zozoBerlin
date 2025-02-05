# Generated by Django 4.1.4 on 2024-07-22 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='notes',
            field=models.TextField(default='', verbose_name='Special Request'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='reservation_terms',
            field=models.BooleanField(default=False, verbose_name='Reservation Terms'),
            preserve_default=False,
        ),
    ]
