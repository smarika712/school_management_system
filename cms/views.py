from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Banner,GalleryCategory,GalleryImage,Event,Announcement,Testimonials
# Create your views here.
def gallery_view(request):
    categories=GalleryImage.objects.prefetch_related('images').all()
    selected_category=request.GET.get('category')
    
    images=GalleryImage.objects.select_related('category','uploaded_by').all()
    paginator = Paginator(images, 12)
    page=request.GET.get('page')
    images= paginator.get_page(page)
    
    
    return render(request,'cms/gallery.html',{
        'categories':categories,'images':images,'selected_category':selected_category    
        })
    
def events_view(request):
    events=Event.objects.filter(is_publish=True)
    event_type=request.GET.get('type')
    if event_type:
        events=events,filter(event_type=event_type)
        paginator=Paginator(events,9)
        page=request.GET.get('page')
        events=paginator.get_page(page)
            
    return render(request,'cms/events.html',{
        'evevts':events,'event_type':Event.EVENT_TYPE ,'selected_type':event_type         
        })
            
def announcements_view(request):
    from django.utils import timezone
    now=timezone.now()
    announcements=Announcement.objects.filter(
        is_published=True
        
    ).filter(
        expires_at__gt=now
    ) | Announcement.objects.filter(
        is_published=True,expires_at__isnull=True
    )
    
    return render(request,'cms/announcements.html',{'announcements':announcements.distinct()})

@login_required
def manage_view(request):
    if not request.user.is_superuser and request.user.profile.role !='admin':
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('Access denied.')
    return render(request,'cms/manage.html',{
        'banners':Banner.objects.all()[:10],
        'categories':Event.objects.all(),
        'events':Event.objects.all()[:10],
        'announcements':Announcement.objects.all()[:10]
    })
    
    