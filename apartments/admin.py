from django.contrib import admin
from .models import Apartment,ApartmentImage, FAQ, Option, Category, Contact, SiteContent,Notification
# Register your models here.

@admin.register(Apartment)
class ApartmentList(admin.ModelAdmin):
    list_display = (
        'title',
        'price_per_night',
        'max_guests',
        'num_bedrooms',
    )
    
    search_fields = ('title',)
    
    list_filter = ('max_guests',)
    
    fieldsets = (
        (None,{
            'fields':('title', 'description', 'location','location_url', 'main_image')
        }),
        ('Details',{
            'fields':('max_guests', 'num_bedrooms', 'area_apartment', 'wifi_availability')
        }),
        ('Pricing',{
            'fields':('price_per_night', 'cleaning_fee', 'discount')
        }),
        ("Features and Images",{
            'fields':('cancellation_hours', 'options')
        }),
        ("Rules and Policies",{
            'fields' :('check_in_time', 'check_out_time', 'house_rules')
        })
    )
    
admin.site.register(ApartmentImage)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_visible')
    list_filter = ('is_visible',)
    search_fields = ('question',)
    
    
class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    fields = ['name', 'icon_svg', 'icon_font_awesome', 'is_main']

class CategoryAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Option)
admin.site.register(Contact)
admin.site.register(SiteContent)
admin.site.register(Notification)

# 
admin.site.site_header = "ZOZO Berlin Admin Panel"
admin.site.site_title = "ZOZO Berlin Admin Panel"
