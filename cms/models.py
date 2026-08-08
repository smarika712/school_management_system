from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Banner(models.Model):
    title= models.CharField(max_length=200)
    subtitle= models.CharField(max_length=300, blank=True)
    image= models.ImageField(upload_to='cms/banner/%Y/%m/')
    link_url= models.URLField(blank=True)
    button_text= models.CharField(max_length=50, blank= True)
    order= models.PositiveBigIntegerField(default=0)
    is_active= models.BooleanField(default=True)
    start_date= models.DateTimeField(null= True, blank=True)
    end_date= models.DateTimeField(null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering= ['order','-created_at']
        
    def __str__(self):
            return self.title
        
class GalleryCategory(models.Model):
    name= models.CharField(max_length=100)
    slug= models.SlugField(max_length=100, unique=True, blank= True)
    is_featured = models.BooleanField(default=False)
    description= models.TextField(blank=True)
    order= models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering=['order','name']
        
    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug= slugify(self.name)
        super().save(*args,**kwargs)
        
class GalleryImage(models.Model):
    category= models.ForeignKey(GalleryCategory, on_delete=models.CASCADE,
    related_name='images')
    title= models.CharField(max_length=200)
    image= models.ImageField(upload_to='cms/gallery/%Y/%m/')
    thumbnail= models.ImageField(upload_to='cms/gallery/%Y/%m/')
    caption= models.CharField(max_length=500, blank=True)
    uploaded_by= models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    is_featured= models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering= ['title']
        
    def __str__(self):
        return self.title
        
class Event(models.Model):
    EVENT_TYPES=[
        ('academic','Academic'),('cultural','Cultural'),
        ('sports','Sports'),('workshop','Workshop'),
        ('holiday','Holiday'),('other','Other'),
    ]  
    
    title= models.CharField(max_length=200)
    slug= models.SlugField(max_length=200, unique= True,blank=True)
    event_type= models.CharField(max_length=20,choices= EVENT_TYPES, default='other')
    description= models.TextField()
    banner_image= models.ImageField(upload_to='cms/events/%Y/%m', blank=True, null=True)
    location= models.CharField(max_length=200,blank=True)
    start_date= models.DateTimeField()
    end_date= models.DateTimeField()
    is_published= models.BooleanField(default= True)
    created_by= models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    uploaded_at= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['-start_date']
        
    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug= slugify(self.title)
        super().save(*args,**kwargs)
        
class Announcement(models.Model):
    PRIORITY_CHOICES=[
        ('low','Low'),('medium','Medium'),
        ('high','High'),('urgent','Urgent'),
    ]
    
    title= models.CharField(max_length=200)
    content= models.TextField()
    priority= models.CharField(max_length=10,choices=PRIORITY_CHOICES, default='medium')
    attachment= models.FileField(upload_to='cms/announcement/%Y/%m', blank=True, null= True)
    is_published= models.BooleanField(default= True)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at= models.DateTimeField(null= True, blank=True)
    created_by= models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    created_at= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering= ['-created_at']
        
    def __str__(self):
        return self.title
    
class Testimonials(models.Model):
    person_name= models.CharField(max_length=200)
    role= models.CharField(max_length=100, help_text='e.g. parent, Alumini,Student')
    quote= models.TextField()
    photo= models.ImageField(upload_to='cms/testimonials/%Y/%m', blank= True, null= True)
    rating= models.PositiveIntegerField(default= 5, help_text='Rating from 1 to 5')
    is_active= models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering= ['-created_at']
        
    def __str__(self):
        return f'{self.person_name}-{self.role}'