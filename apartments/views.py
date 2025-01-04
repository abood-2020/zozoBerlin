from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Apartment, FAQ, SiteContent
from reservation.models import Review
from .forms import ContactForm
from django.db.models import Avg, Count

# Create your views here.

def index(request):
    apartments = Apartment.objects.all()[:3]
    apartment1 = apartments[0] if len(apartments) > 0 else None
    apartment2 = apartments[1] if len(apartments) > 1 else None
    apartment3 = apartments[2] if len(apartments) > 2 else None
    
    # to get on images to every apartments 
    images1 = apartment1.images.all() if apartment1 != None else None
    images2 = apartment2.images.all() if apartment2 != None else None
    images3 = apartment3.images.all() if apartment3 != None else None
    questions = FAQ.objects.filter(is_visible = True)[:5]
    site_content = SiteContent.objects.first()
    
    reviews = Review.objects.all()[:4]
    reviews_data = []
    for review in reviews:
        profile = review.user.myprofile if review.user else None  
        reviews_data.append({
            'name': review.name,
            'profile_image': profile.image.url if profile and profile.image else None,
            'address': profile.address if profile else None,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at,
        })
    context = {
        'apartment1': apartment1,
        'images_1' : images1 ,
        'apartment2': apartment2,
        'images_2' : images2 ,
        'apartment3': apartment3,
        'images_3' : images3 ,
        'reviews' : reviews_data,
        'FAQ' : questions,
        'apartments': apartments,
        'site_content':site_content,
    }
    return render(request, "index.html", context)

def about_us(request):
    apartments = Apartment.objects.all()[:3]
    context = {"apartments": apartments,}
    return render(request,"imprint.html", context)

def terms_privacy_view(request):
    return render(request,'terms.html')

def apartment_view(request, apartment_id):
    apartment = get_object_or_404(Apartment, id = apartment_id)
    apartment_options = apartment.options.all()
    three = apartment.images.all()[:3]
    images = apartment.images.all()
    reviews = Review.objects.filter(apartment__pk=apartment.pk)
    reviews_stats = Review.objects.filter(apartment__pk=apartment.pk).aggregate(average_rating=Avg('rating'), total_reviews=Count('id'))
    reviews_data = []
    for review in reviews:
        profile = review.user.myprofile if review.user else None  
        reviews_data.append({
            'name': review.name,
            'profile_image': profile.image.url if profile and profile.image else None,
            'address': profile.address if profile else None,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at,
        })
    print(images)
    context = {
        'object' : apartment,
        'apartment_options': apartment_options,
        'three' : three,
        'images' : images,
        'reviews': reviews_data,
        'average_rating': reviews_stats['average_rating'],
        'total_reviews': reviews_stats['total_reviews'],

    }
    return render(request,"apartment_view.html",context)

def contact_us(request):
    success_message = ""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the form data as a record in the Contact model
            success_message = "Thank you for your message! We will respond to your email as soon as possible."
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form, 'success_message': success_message})

def contact_success_view(request):
    return render(request, 'contact_success.html')

def terms(request):
    return render(request, 'terms.html')

def FAQ_views(request):
    questions_booking = FAQ.objects.filter(is_visible = True, category='booking')[:5]
    questions_payment = FAQ.objects.filter(is_visible = True, category='payment')[:5]
    context = {
        'FAQ_booking' : questions_booking,
        'FAQ_payments' : questions_payment,
    }
    return render(request, "FAQ.html", context)

def page_404(request):
    return render(request, '404.html')
