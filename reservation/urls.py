from django.urls import path 
from . import views

urlpatterns = [
    path("<int:apartment_id>", views.reservation_form, name="reservation_page"),
    path('payment/<int:reservation_id>', views.payment_view, name='payment_form'),
    path('charge/', views.charge, name='charge'),
    path("success/<int:reservation_id>", views.confirm_reservation, name="success_confirm_booking"),
    path('reservations/<int:reservation_id>/details/', views.reservation_details, name='reservation_details'),
    path('confirm/<int:reservation_id>', views.booking_confrimation, name='booking_confirmation'),
    path('update_booking_staus/', views.update_reservation_status, name="update_booking_status"),
    path('cancel_booking/', views.cancel_reservation , name="cancelation_booking"),
    path('delete_review/', views.delete_reivew , name="delete_review"),
    path('check-existing-reservation/', views.check_existing_reservation, name='check_existing_reservation'),

]
