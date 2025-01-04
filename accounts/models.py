from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
            
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='myprofile')
    phone_number = models.CharField(max_length=15, null=True)
    image = models.ImageField(upload_to ='ImagesUser/', null=True, blank=True)
    address = models.CharField(max_length=255,null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

            
    
            


