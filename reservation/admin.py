from django.contrib import admin
from .models import Reservation, Review,Payment
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Register your models here.

admin.site.register(Review)

@admin.register(Reservation)
class ReservationList(admin.ModelAdmin):
    list_display = (
        'user',
        'apartment',
        'start_date',
        'end_date',
        'total_price',
        'status',
        'updated_at',
    )
    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        for req in queryset:
            req.approve()
            req.booking_deposit_email()
            
        self.message_user(request, "The selected requests have been approved.")

    approve_requests.short_description = "Approve selected requests"

    search_fields = ('user', 'apartment')
    
    list_filter = ('status',)
    
    readonly_fields = ('total_price','num_night',)
    
@admin.register(Payment)
class PaymentList(admin.ModelAdmin):
    list_display = (
        'user',
        'reservation',
        'date',
        'amount',
        'status'
    )
    
