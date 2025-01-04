from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="main_page"),
    path("apartment/<int:apartment_id>", views.apartment_view, name="apartment_view"),
    path("Imprint", views.about_us, name="Imprint"),
    path("contact-us", views.contact_us, name="contact_us"),
    path('contact-success/', views.contact_success_view, name='contact_success'),
    path("terms", views.terms, name="terms"),
    path("FAQ", views.FAQ_views, name="FAQ"),
    path("404", views.page_404, name="404_page"),
    path("terms-of-use", views.terms_privacy_view, name="terms_to_use")
]