import stripe
from django.shortcuts import get_object_or_404, render , redirect , HttpResponse
from apartments.models import Apartment
from reservation.models import Reservation,Review
from .forms import ReservationForm, PaymentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from project import settings
from datetime import datetime,date, timedelta
from apartments.utils import create_notification

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

def reservation_form(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    user = request.user
    current_year_start = date(date.today().year, 1, 1)
    current_date = date.today()

    reservations = Reservation.objects.filter(apartment=apartment).exclude(status='cancelled').order_by('start_date')
    reservation_dates = [(reservation.start_date, reservation.end_date) for reservation in reservations]    
    reservation_dates.append((current_year_start, current_date))

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.apartment = apartment
            reservation.total_price = 100
            reservation.save()  # Save the reservation to the database

            return redirect('booking_confirmation' , reservation_id = reservation.id )
        else:
            print(form.errors)  # Print form errors if the form is not valid
    else:
        form = ReservationForm()
    context = {
        "apartment": apartment,
        "apartment_guest" : range(1, int(apartment.max_guests +1)),
        "form": form,
        'name_page' : "reservation",
        "reservation_date" : reservation_dates,
        
    }
    return render(request, "booking_form.html", context)
    
@csrf_exempt
def update_reservation_status(request):
    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        try:
            reservation = get_object_or_404(Reservation, id =reservation_id)
            reservation.status = 'pending_approval'
            reservation.save()
            create_notification(
                user=reservation.user,
                notification_type='pending_request',
                message=f"Your booking request for the apartment '{reservation.apartment.title}' is pending approval."
            )
            return JsonResponse({'success':True})
        except Reservation.DoesNotExist:
            return JsonResponse({'success':False, 'error': 'Reservation not found'})
    return JsonResponse({'success':False, 'error':'Invalid request method'})

@csrf_exempt
def cancel_reservation(request):
    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        try:
            reservation = get_object_or_404(Reservation, id=reservation_id)
            reservation.status = 'cancelled'
            reservation.save()
            reservation.send_cancel_email()
            create_notification(
                user=reservation.user,
                notification_type='cancel_confirmation',
                message=f"Your booking for the apartment '{reservation.apartment.title}' has been canceled."
            )
            return JsonResponse({'success': True})
        except Reservation.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Reservation not found'})
    return JsonResponse({'success': False, 'error': "Invalid request method"})

@csrf_exempt
def delete_reivew(request):
    if request.method == "POST":
        review_id = request.POST.get('review_id')
        print("Not Fount ===============")
        print(review_id)

        try:
            review = get_object_or_404(Review, id =review_id)
            print("Not Fount ===============")
            print(review_id)
            review.delete()
            return JsonResponse({'success': True})
        except Review.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Review not found'})
    return JsonResponse({'success': False, 'error': "Invalid request method"})

def reservation_details(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    data = {
        'number': reservation.number,
        'start_date': reservation.start_date,
        'end_date': reservation.end_date,
        'apartment': reservation.apartment.name,
        'total_price': reservation.total_price,
        'status': reservation.status,
    }
    return JsonResponse(data)

def payment_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        print(form.errors)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.reservation = reservation
            payment.status = 'paid'
            payment.save();
            reservation.status = 'confirmed'
            reservation.save()
            return redirect('success_confirm_booking',reservation_id = reservation.id )
    else :
        pass 
        # form = PaymentForm()
    return render(request, 'payment_form.html', {
        # 'form' : form,
        'object' : reservation,
    })
    
@csrf_exempt
def charge(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=3000,  # المبلغ بالسينتات (30 دولارًا)
                currency='usd',
                description='Example charge',
                source=token,
            )
            return JsonResponse({'status': 'success'})
        except stripe.error.CardError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def confirm_reservation(request, reservation_id):
    return render(request, "success_booking.html")

def booking_confrimation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    context = {'object': reservation}
    return render(request, "booking_confirmation.html",context)

def check_existing_reservation(request):
    user = request.user
    print("=====================> start new function")
    # Check for unconfirmed reservations
    has_unconfirmed_reservation = Reservation.objects.filter(
        user=user,
        status__in=['pending_approval', 'pending']
    ).exists()
    
    # Return JSON response
    return JsonResponse({
        'has_unconfirmed_reservation': has_unconfirmed_reservation
    })