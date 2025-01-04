from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('profile', views.update_profile, name="Profile"),
    path("myReservation", views.reservation_list, name="reservation_list"),
    path("Notifications", views.notifications_view, name="notifications"),
    path("myPayment", views.payment_list, name="payment_list")   ,
    path('register/', views.signup, name='register'),
    path('login/', views.login_view, name='login'),
    path('booking-details/<int:reservation_id>',views.booking_details, name="booking_details"),
    path('booking/<int:booking_id>/review', views.add_review, name="submit_review"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path("change_password",auth_views.PasswordChangeView.as_view(template_name="chanag_password.html"), name="change_password"),
    path("change_password/done",auth_views.PasswordChangeDoneView.as_view(template_name="chanag_password_done.html"), name="change_password_done"),
    path('notifications/count/', views.notifications_count, name='notifications_count'),

]