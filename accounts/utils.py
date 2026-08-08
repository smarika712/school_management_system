from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def send_verification_email(user, verification_url):
    subject = 'Verify Your Email - SATRI'
    context = {'user':user,'verification_url':verification_url,'school_name':'SATRI'}
    html_message=render_to_string('accounts/email/verify_email.html',context)
    plain_message=strip_tags(html_message)
        
        
    email=EmailMultiAlternatives(
        subject=subject,body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL, to=[user.email]
        
        
    )
    
    email.attach_alternative(html_message,'text/html')
    email.send(fail_silently=False)
    
def send_welcome_email(user):
    subject='Welcome to SATRI'
    context ={'user':user,"school_name":'SATRI  '}
    html_message=render_to_string('accounts/email/welcome.html',context)
    plain_message = strip_tags(html_message)
    
    email=EmailMultiAlternatives(
        subject=subject,body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,to=[user.email],
)
    
    email.attach_alternative(html_message,'text/html')
    email.send(fail_silently=False)
    