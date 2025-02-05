# Generated by Django 4.1.4 on 2024-08-10 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0003_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='num_guest',
            field=models.IntegerField(default=0, verbose_name='Guests'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('pending_approval', 'Pending Approval'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', help_text='Status of the reservation.', max_length=20, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(help_text='User who made the reservation.', on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL, verbose_name='Tenant Name'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('currency', models.CharField(default='USD', max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Payment Date')),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending'), ('declined', 'Declined ')], default='Draft', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='reservation.reservation', verbose_name='Reservation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='Tenant Name')),
            ],
        ),
    ]
