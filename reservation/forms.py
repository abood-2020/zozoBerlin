from django import forms 
from .models import Reservation, Payment

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'start_date',
            'end_date',
            'total_price',
            'notes',
            'num_guest',
            'reservation_terms',
        ]

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'amount',
            'payment_options'
        ]
        
