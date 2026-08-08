from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'you@example.com'
            }))

    first_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            } ))

    last_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }
        )
    )


    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists")

        return email



# Keep this outside UserRegistrationForm
class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username or email',
                'autofocus': True
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )