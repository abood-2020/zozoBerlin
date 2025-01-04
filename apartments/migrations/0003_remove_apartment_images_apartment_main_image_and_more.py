# Generated by Django 4.1.4 on 2024-07-19 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0002_apartment_area_apartment_apartment_wifi_availability'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='images',
        ),
        migrations.AddField(
            model_name='apartment',
            name='main_image',
            field=models.ImageField(default='', help_text='Upload Main Page to this Apartment.', upload_to='apartment_images/', verbose_name='Main Image'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ApartmentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title of Image')),
                ('description', models.CharField(max_length=255, verbose_name='Description About Image')),
                ('image', models.ImageField(upload_to='apartment_images/')),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='apartments.apartment')),
            ],
        ),
    ]
