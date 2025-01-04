from django.db import models
from django.contrib.auth.models import User
from apartments.models import Apartment
from django.core.mail import send_mail
from project import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from apartments.utils import create_notification

# Create your models here.
class Reservation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservations',
        help_text="User who made the reservation.",
        verbose_name ="Tenant Name"
    )
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name = "reservations",
        help_text ="Apartment being reserved.",
        verbose_name="Apartment"
    )
    start_date = models.DateField(
        help_text ="Start date of the reservation",
        verbose_name="Start Date"
    )
    end_date = models.DateField(
        help_text="End date of the reservation.",
        verbose_name="End Date"
    )
    num_night = models.IntegerField(
        help_text= "Number of Nights",
        verbose_name="Number Of Night"
    )
    total_price = models.DecimalField(
        max_digits = 10,
        decimal_places=2,
        default= 0 ,
        help_text ="Total Price for the reservations.",
        verbose_name="Total Price",
        null = True,
        blank=True
    )
    num_guest = models.IntegerField(
        verbose_name="Guests"
    )
    reservation_terms = models.BooleanField(
        verbose_name= "Reservation Terms"
    )
    notes = models.TextField(
        verbose_name="Special Request"
    )
    sub_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Sub Total",
    )
    services_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Services Fee",
    )

    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00, 
        help_text="Discount"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text ="Date and time when the reservation was created",
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now = True,
        help_text="Date and Time when the reservation was updated.",
        verbose_name ="Updated At"
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending','Pending'),
            ('pending_approval', 'Pending Approval'),
            ('confirmed', 'Confirmed'),
            ('cancelled','Cancelled')
        ],
        default = 'pending',
        help_text ="Status of the reservation.",
        verbose_name="Status"
    )
    
    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            # Calculate the number of nights
            num_nights = (self.end_date - self.start_date).days
            
            # Get the price per night from the apartment
            price_per_night = float(self.apartment.price_per_night)
            
            # Ensure the number of nights is positive
            if num_nights > 0:
                # Set the service fee
                self.services_fee = self.apartment.cleaning_fee
                
                # Calculate the subtotal
                sub_total = num_nights * price_per_night
                
                # Apply an 8% discount if staying more than 7 nights
                # if num_nights > 7:
                #     discount_amount = sub_total * 0.08  # Calculate 8% discount
                #     self.discount = sub_total - discount_amount  # Set the discount amount
                # else:
                #     self.discount = 0.0  # No discount for stays of 7 nights or less
                
                # Set the total price
                self.total_price = sub_total
                self.sub_total = sub_total
                # Set the number of nights
                self.num_night = num_nights
                print()
        # Call the parent class's save method to apply changes
        super(Reservation, self).save(*args, **kwargs)    
  
    def __str__(self):
        return f'Reservation {self.id} by {self.user.username}'
    
    def approve(self):
        self.status = 'confirmed'
        create_notification(
            user=self.user,
            notification_type='booking_confirmation',
            message=f"Your booking for the apartment '{self.apartment.title}' has been confirmed."
        )
        self.save()

    def send_confirm_email(self):

        # Prepare the context for the email template
        context = {
            'name': self.user.first_name,
            'apartment_name': self.apartment.title,
            'check_in_date': self.start_date,
            'check_out_date': self.end_date,
            'number_of_guests': self.num_guest,
            'nightly_rate': self.apartment.price_per_night,
            'check_in_time': self.apartment.check_in_time,
        }
        
        # Render the HTML content for the email
        html_content = render_to_string('Emails/confirm_email.html', context)

        # Create and send the email
        email = EmailMessage(
            subject="ZOZO Berlin : Booking Confirmation",
            body=html_content,
            from_email='abdrazzaq20182019@gmail.com',
            to=[self.user.email]
        )
        email.content_subtype = "html"

        try:
            email.send()
        except Exception as e:
            # Handle any exceptions that occur during email sending
            print(f"Failed to send email: {e}")
    
    def send_cancel_email(self):
    
        # Prepare the context for the email template
        context = {
            'name': self.user.first_name,
            'apartment_name': self.apartment.title,
        }
        
        # Render the HTML content for the email
        html_content = render_to_string('Emails/cancel_booking_emails.html', context)

        # Create and send the email
        email = EmailMessage(
            subject="ZOZO Berlin : Booking Cancel",
            body=html_content,
            from_email='abdrazzaq20182019@gmail.com',
            to=[self.user.email]
        )
        email.content_subtype = "html"

        try:
            email.send()
        except Exception as e:
            # Handle any exceptions that occur during email sending
            print(f"Failed to send email: {e}")    
    
    def booking_deposit_email(self):
            
        # Prepare the context for the email template
        context = {
            'name': self.user.first_name,  # الاسم الأول للمستخدم
            'apartment_name': self.apartment.title,  # عنوان الشقة
            'total_cost': self.total_price,  # التكلفة الإجمالية للحجز
            'deposit_amount': self.total_price * 0.30,  # 30% من التكلفة الإجمالية
            'id_booking':self.id
        }
        # Render the HTML content for the email
        html_content = render_to_string('Emails/Booking_deposit_reminder.html', context)

        # Create and send the email
        email = EmailMessage(
            subject="ZOZO Berlin:Confirm Your Booking - Action Required",
            body=html_content,
            from_email='abdrazzaq20182019@gmail.com',
            to=[self.user.email]
        )
        email.content_subtype = "html"

        try:
            email.send()
        except Exception as e:
            # Handle any exceptions that occur during email sending
            print(f"Failed to send email: {e}")    

    
    class Meta:
        ordering =['-created_at']

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('declined', 'Declined ')
    ]
    PAYMENT_OPTIONS = [
        ('deposit', 'Deposit'),
        ('full_payment', 'Full Payment')
    ]
    user = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name = 'payments',
        verbose_name="Tenant Name"
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete= models.CASCADE,
        related_name = 'payments',
        verbose_name = "Reservation",
    )
    payment_options = models.CharField(
        choices= PAYMENT_OPTIONS,
        max_length=30
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amount",
    )
    currency = models.CharField(
        max_length=10,
        default='USD'
    )
    date = models.DateTimeField(
        auto_now_add = True,
        verbose_name= "Payment Date"
    )
    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00, 
        help_text="Discount"
    )
    status = models.CharField(
        max_length=20,
        choices= PAYMENT_STATUS_CHOICES,
        default='Draft'
    )
    
    created_at = models.DateTimeField(
        auto_now_add = True
    )
    updated_at = models.DateTimeField(
        auto_now = True,
    )
    
    def __str__(self):
        return f"Payment {self.id} - Reservation {self.reservation_id}"
    
class Review(models.Model):
    REVIEW_METHOD = [
            ('by_user','By User'),
            ('by_airbnb', 'From Airbnb'),
            ('by_booking', 'From Booking'),
        ]
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50,)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    review_method = models.CharField(choices=REVIEW_METHOD,default="by_user",max_length=30)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.reservation:
            return f'Review by {self.name} for {self.reservation.apartment.title}'
        return f'Review by {self.name} for {self.apartment.title}'
    
    def save(self, *args, **kwargs):
        if self.user:
            self.name = self.user.first_name + " " + self.user.last_name
        if self.reservation:  # If there is a reservation, automatically set the apartment
            self.apartment = self.reservation.apartment
        elif not self.apartment:  # If no reservation and apartment is missing, raise error
            raise ValueError("Apartment must be selected if no reservation is provided.")
        super().save(*args, **kwargs)
