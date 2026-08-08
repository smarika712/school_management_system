from django.shortcuts import render, redirect
from django.conf import settings
from .forms import UserRegistrationForm, LoginForm
from .tokens import (
    get_tokens_for_users, generate_email_verification_token,
    verify_email_token, get_user_from_uidb64
)
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .utils import send_verification_email, send_welcome_email
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save() 
 
            token = generate_email_verification_token(user)
            user.profile.email_verification_token = token
            user.profile.save()
 
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = f'{settings.FRONTEND_URL}/accounts/verify-email/{uid}/{token}/'
 
            try:
                send_verification_email(user, verification_url)
                messages.info(request, f'Account created! Verification link sent to {user.email}')
            except Exception as e:
                messages.warning(request, f'Account created but email could not be sent: {str(e)}')
 
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
 
 
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
 
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                tokens = get_tokens_for_users(user)
                request.session['access_token'] = tokens['access']
                request.session['refresh_token'] = tokens['refresh']
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect(request.GET.get('next', 'dashboard'))
            messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
 
    return render(request, 'accounts/login.html', {'form': form})
 
 
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')
 
 
def verify_email_view(request, uidb64, token):
    user = get_user_from_uidb64(uidb64)
    if user is not None and verify_email_token(user, token):
        user.profile.is_email_verified = True
        user.profile.email_verification_token = ''
        user.profile.save()
        send_welcome_email(user)
        messages.success(request, 'Email verified! You can now log in')
        return redirect('login')
    messages.error(request, 'Invalid or expired verification link')
    return redirect('home')
 
 
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
        'user': request.user,
        'profile': request.user.profile,
        'access_token': request.session.get('access_token')
    }
    return render(request, 'accounts/dashboard.html', context)
 
 
@require_POST
def api_token_refresh(request):
    """Refresh JWT token pair via AJAX"""
    refresh_token = request.session.get('refresh_token')
    if not refresh_token:
        return JsonResponse({'error': 'No refresh token'}, status=401)
    try:
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken(refresh_token)
        new_access = str(refresh.access_token)
        request.session['access_token'] = new_access
        return JsonResponse({'access': new_access})
    except Exception:
        return JsonResponse({'error': 'Token refresh failed'}, status=401)
 