from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Option(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon_svg = models.TextField(blank=True, null=True)  # SVG CODE
    icon_font_awesome = models.CharField(max_length=100, blank=True, null=True)  # Font Awseome
    is_main = models.BooleanField(default=False)  # حقل لتحديد إذا كان الخيار رئيسي

    def __str__(self):
        return self.name

class Apartment(models.Model):
    title = models.CharField(
        max_length=255,
        unique=1,
        help_text="Title of the apatment (must be unique)",
        verbose_name="Apartment Title"
    )
    
    description = models.TextField(
        help_text = "Detailed Description of the apartment",
        verbose_name = "Description"
    )
    
    promotional_text = models.CharField(
        help_text = "Writing a promotional text about the apartment",
        verbose_name = "Promotional Text",
        max_length=30,
        null=True,
        blank=True
    )
    
    location_url = models.URLField(
        max_length=300,
        blank=True,
        null=True,
        help_text ="Location of the apartment",
        verbose_name = "Location")
    
    location = models.CharField(max_length=100, verbose_name="Location")


    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price per night in USD",
        verbose_name="Price per Night"
    )
    
    max_guests = models.IntegerField(
        help_text = "Maximum number of guests allowed",
        verbose_name = "Max Guest",
    )
    
    num_bedrooms = models.IntegerField(
        help_text= "Number of bedrooms in the apartment.",
        verbose_name="Number of Bedrooms"
    )
    
    wifi_availability = models.BooleanField(
        help_text ="Check False is Wifi Not Avaibility",
        verbose_name = "Wifi Availability",
        default=True
    )
    
    area_apartment = models.IntegerField(
        help_text = "Area of Apartment",
        verbose_name = "Area",
    )
        
    main_image = models.ImageField(
        help_text="Upload Main Page to this Apartment.",
        verbose_name="Main Image",
        upload_to = "apartment_images/"
    )
    
    check_in_time = models.TimeField(
        help_text = "Check-in time",
        verbose_name = "Check-in Time"
    )
    
    check_out_time = models.TimeField(
        help_text="check-out time",
        verbose_name="Check-out Time"
    )
    
    house_rules = models.TextField(
        help_text = "House rules for the apartment",
        verbose_name="House Rules"
    )
    options = models.ManyToManyField(Option, related_name='apartments')
    
    cancellation_hours = models.IntegerField(
        verbose_name= "Cancellation Days",
        default=24
    )
    cleaning_fee = models.DecimalField(
        verbose_name="Cleaning Fee",
        default = 70,
        max_digits=6,
        decimal_places=2,
    )
    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00, 
        help_text="Discount percentage for the passenger (e.g., 10.50 for 10.5%)"
    )
    
    
    def __str__(self):
        return self.title
    
class ApartmentImage(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        related_name='images',
        on_delete=models.CASCADE
    ) 
    
    title = models.CharField(
        max_length=50,
        verbose_name="Title of Image"
    )
    
    description = models.CharField(
        max_length=255,
        verbose_name="Description About Image",
        null = True,
        blank=True 
    )
    
    image = models.ImageField(
        upload_to="apartment_images/"
    )
    
    def __str__(self):
        return f"Image for {self.apartment.title} : {self.title}"
   
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    category = models.CharField(max_length=20,choices=[
            ('booking','Booking'),
            ('payment', 'Payments'),
        ])
    answer = models.TextField()
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.question

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SiteContent(models.Model):
    contact_email = models.EmailField(max_length=254, verbose_name="Contact Email")
    contact_phone = models.CharField(max_length=20, verbose_name="Contact Phone")
    legal_phone = models.CharField(max_length=20, verbose_name="Legal Phone")
    legal_email = models.EmailField(max_length=254, verbose_name="Legal Email")
    vat_id = models.CharField(max_length=20, verbose_name="Vat ID")
    location = models.CharField(max_length=100, verbose_name="Location")
    
    
    def save(self, *args, **kwargs):
        if SiteContent.objects.exists() and not self.pk:
            raise ValidationError("You can only create one SiteContent record.")
        super(SiteContent, self).save(*args, **kwargs)

    def __str__(self):
        return "Site Content"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('booking_confirmation', 'Booking Confirmation'),
        ('cancel_confirmation', 'Booking Cancel'),
        ('pending_request', 'Pending Request'),
        ('booking_modification', 'Booking Modification'),
        ('deposit_payment', 'Deposit Payment'),
        ('upcoming_date', 'Upcoming Date'),
        ('service_review', 'Service Review'),
        ('complete_information', 'Complete Information'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"
