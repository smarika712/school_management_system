from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES=[
        ('student','Student'),
        ('teacher','Teacher'),
        ('admin','Admin')
    ]
    
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default='student')
    phone_number=models.CharField(max_length=20,blank=True)
    avatar=models.ImageField(upload_to='profile/%Y/%m',blank=True)
    bio=models.TextField(blank=True)
    is_email_verified=models.BooleanField(default=False)
    email_verification_token=models.CharField   (max_length=255,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username}  ({self.get_role_display})'
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
    
    
