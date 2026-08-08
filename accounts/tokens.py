from django.conf import settings
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode ,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def get_tokens_for_users(user):
    """Generate JWT access and refresh tokens for a user"""
    refresh=RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }
    
class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return(
            str(user.pk)+str(timestamp)+str(user.profile.is_email_verified)
        )
        
email_token_generator= EmailVerificationTokenGenerator()

def generate_email_verification_token(user):
    return email_token_generator.make_token(user)

def verify_email_token(user,token):
    return email_token_generator.check_token(user,token)

def get_user_from_uidb64(uidb64):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        return User.objects.get(pk=uid)
    except(TypeError,ValueError,User.DoesNotExist):
        return None
    
    