from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
# Register your models here.


class ProfileInline(admin.StackedInline):
    model=Profile
    can_delete=False
    fields=('role','phone_number','bio','avatar','is_email_verified')
    
    
class CustomerUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display=('username','email','first_name','last_name','is_active','is_staff','get_role')
    list_filter=('is_active','is_staff','profile__role')
        
        
    def get_role(self,obj):
        try:
            return obj.profile.get_role_display()
        except Profile.DoesNotExist:
            return '-'
    get_role.short_description='Role'
            
admin.site.unregister(User)
admin.site.register(User,CustomerUserAdmin)