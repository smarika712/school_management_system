from django.contrib import admin
from .models import Banner,GalleryCategory,GalleryImage,Event,Announcement,Testimonials
# Register your models here.


class BannerAdmin(admin.ModelAdmin):
    list_display=('title','order','is_active','start_date','end_date')
    list_filter=('is_active')
    list_editable=('order','is_active')
    readonly_fields=('created_at',)
    
    @admin.register(GalleryCategory)
    class GalleryCategoryAdmin(admin.ModelAdmin):
        list_display=('name','slug','order')
        prepopulated_fields={'slug':('name',)}
        list_editable=('order',)
        
    @admin.register(GalleryImage)
    class GalleryImageAdmin(admin.ModelAdmin):
        list_display=('title','category','uploaded_by','is_featured')
        list_filter=('category','is_featured')
        search_fields=('title','caption')
        list_editable=('is_featured',)
        readonly_fields=('uploaded_at',)
    
    @admin.register(Event)
    class EventAdmin(admin.ModelAdmin):
        list_display=('title','event_type','location','start_date','is_published')
        list_filter=('event_type','is_published')
        search_fields=('title','description')
        prepopulated_fields={'slug':('title',)}
        list_editable=('is_published',)
        readonly_fields=('uploaded_at',)
            
    @admin.register(Announcement)
    class AnnouncementAdmin(admin.ModelAdmin):
        list_display=('title','priority','is_published','published_at','expires_at')
        list_filter=('priority','is_published')
        search_fields=('title','content')
        list_editable=('priority','is_published')
        readonly_fields=('created_at',)
            
            
    @admin.register(Testimonials)
    class TestimonialsAdmin(admin.ModelAdmin):
        list_display=('person_name','role','rating','is_active','created_at')
        list_filter=('is_active','rating')
        search_fields=('is_active','rating')
        list_editable=('is_active',)
        readonly_fields=('created_at',)