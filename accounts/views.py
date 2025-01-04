from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from reservation.models import Reservation,Payment
from apartments.models import Apartment,Notification
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, ProfileForm, LoginForm, UserForm,ProfileImageForm
from reservation.models import Review
from .models import Profile
from datetime import datetime
from django.http import JsonResponse
from apartments.utils import create_notification

def signup(request):
    user_form = None
    profile_form = None
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            create_notification(
                user=user,
                notification_type='complete_information',
                message="Please complete your registration information to continue using our services."
            )

            # profile = Profile.objects.get(user=user)
            # profile_form = ProfileForm(request.POST, instance=profile)
            # profile_form.save()
            
            user = authenticate(username=user.username, password=user_form.cleaned_data['password'])
            login(request, user)
            return redirect('dashboard')
        
    else:
        user_form = UserRegistrationForm()
        # profile_form = ProfileForm()

    context = {
        'form': user_form,
    }
    return render(request, 'signup.html',context)
        
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html',{'form':form})

@login_required
def notifications_count(request):
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})

            
@login_required
def dashboard(request):
    today = datetime.now().date()
    print(today)
    booking = Reservation.objects.filter(user=request.user, start_date__gte=today).exclude(status='cancelled').first()
    apartments = Apartment.objects.all()[:3]
    # Fetch notifications for the user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark notifications as read
    notifications.filter(is_read=False).update(is_read=True)

    context = {
        'booking': booking,
        'name_page':"dashboard",
        'payments': None,
        'apartmnets' : apartments,
        'notifications': notifications
    }
    return render(request, 'dashboard.html', context)

@login_required
def reservation_list(request):
    user_reservations = Reservation.objects.filter(user = request.user)
    context = {
        'user_reservations': user_reservations,
        'name_page' : "myReservation"
    }
    return render(request, "reservation_list.html", context)

@login_required
def payment_list(request):
    payments = Payment.objects.filter(user = request.user)
    context = {
        'payments': payments,
        'name_page' : "myPayment"
    }
    return render(request, "payment_list.html", context)
    
@login_required
def booking_details(request, reservation_id):
    reservation = get_object_or_404(Reservation, id = reservation_id)
    payments = reservation.payments.all()
    review = Review.objects.filter(reservation=reservation)
    context = {
        'object':reservation,
        'payments':payments,
        'name_page' : "BookingDetails",
        'review':review.first()}
    return render(request, "booking_details.html", context)

@login_required
def add_review(request,booking_id):
    current_booking = get_object_or_404(Reservation, id=booking_id)
    user = request.user
    
    if Review.objects.filter(reservation=current_booking):
        return render(request,'error.html',{'message': 'You have already submitted a review for this reservation.'})
    
    if request.method == "GET":
        rating_value = request.GET.get('rating')
        comment = request.GET.get('comment')
        print(rating_value)
        Review.objects.create(
            reservation=current_booking,
            user=user,
            rating=int(rating_value),
            comment=comment,
        )
        return redirect('booking_details' , reservation_id = current_booking.id )

@login_required
def notifications_view(request):
    return render(request, "notifications.html")

@login_required
def update_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    user = request.user
    update_success = False
    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        profile.phone_number = request.POST.get('phone_number')
        profile.address = request.POST.get('address')
        profile.date_of_birth = request.POST.get('birth_date')

        user.save()
        profile.save()
        update_success = True
        
    context = {
        "profile": profile,
        "update_success": update_success,
        'name_page' : "profile"

    }
    print(update_success)
    return render(request, "profile.html", context)
    
