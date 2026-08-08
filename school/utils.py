import os
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image
# from config.urls import urlpatterns

def compress_image(image_file,max_width=None,max_height=None,quality=None):
    """Compress an image file while maintaining aspect ratio"""
    
    max_width=max_width or getattr(settings,'IMAGE_MAX_WIDTH',1920)  
    max_height=max_height or getattr(settings,'IMAGE_MAX_HEIGHT',1080)  
    quality=quality or getattr(settings,'IMAGE_QUALITY ',85)
    
    
    
    img=Image.open(image_file)
    if img.mode in ('RGBA','p'):
        img=img.convert('RGB')
        
        
    original_width,original_height=img.size
    if original_width>max_width or original_height>max_height:
        ratio=min(max_width/original_width,max_height/original_height)
        new_size=(int(original_width*ratio),int(original_height*ratio))
        
        
        img=img.resize(new_size,Image.LANCZOS)
        
    buffer=BytesIO()
    img.save(buffer,format='JPEG',quality=quality,optimize=True)
    buffer.seek(0)
    return ContentFile(buffer.read())
def generate_thumbnail(image_file,size=None):
    """Genertae asquare thumbnail from an image"""
    
    size=size or getattr(settings,'THUMBNAIL_SIZE',300)        
    
    img=Image.open(image_file)
    if img.mode in('RGBA','P'):
       img=img.comvert('RGB')
       
    img.thumbnail((size,size),Image.LANCZOS) 
    buffer=BytesIO()
    
    img.save(buffer,format='JPEG',quality=80,optimize=True)
    buffer.seek(0)
    return ContentFile(buffer.read())
    
def get_file_size_display(size_in_bytes):
    """Convert bytes to a human readable string"""
    
    for unit in ['B','KB','MB','GB']:
        if size_in_bytes<1024:
            return f'{size_in_bytes:1f}  {unit}'
        size_in_bytes/=1024
    return f'{size_in_bytes:.1f} TB'

def validate_file_size(uploaded_file,max_size_mb=10):
    """Validate uploaded file size."""
    max_size=max_size_mb*1024*1024
    if uploaded_file.size > max_size:
        return False , f'File must be less than {max_size_mb}MB, Yours is {get_file_size_display(uploaded_file.size)}'
    return True, None

ALLOWED_IMAGE_TYPES=['image/jpeg','image/png','image/webp','image/gif']
ALLOWED_DOCUMENT_TYPES=[
     'application/pdf','image/jpeg','image/png'
     'applicatyion/msword',
     'application/vnd.openxmlformats-officedocumnet.wordprocessingml.document'
]

def validate_image_type(uploaded_file):
    """Validate that uploaded file is an allowed image type"""
    content_type=getattr(uploaded_file,'content_type',None)
    if content_type and content_type not in ALLOWED_DOCUMENT_TYPES:
            return False , f'Only JPEG ,PNG,WebP,  and GIF allowed.Ypu uploaded{content_type}.'
    return True,None    