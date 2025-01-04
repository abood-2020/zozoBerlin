from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    
    list_display = (
        "user",
        "phone_number",
    )
    search_fields = (
        "user",
    )