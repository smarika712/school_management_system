from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('verify-email/<str:uidb64>/<str:token>/',views.
         verify_email_view,name='verify_email'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('api/token-refresh/',views.api_token_refresh,name='api_token_refresh'),
]
