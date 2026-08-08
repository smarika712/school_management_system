from django.urls import path
from . import views


urlpatterns = [
    path('gallery/',views.gallery_view,name='gallery'),
    path('events/',views.events_view,name='events'),
    path('announcements/',views.announcements_view,name='announcements'),
    path('manage/',views.manage_view,name='manage'),
]