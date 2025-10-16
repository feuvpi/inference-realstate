from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration with email-based authentication.
    Uses crispy forms for Bootstrap styling.
    """
    
    email = forms.EmailField(
        label=_('Email Address'),
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com',
            'autocomplete': 'email'
        })
    )
    
    name = forms.CharField(
        label=_('Full Name'),
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'John Doe',
            'autocomplete': 'name'
        })
    )
    
    company = forms.CharField(
        label=_('Nome da Empresa'),
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Company (opcional)',
            'autocomplete': 'organization'
        })
    )
    
    phone = forms.CharField(
        label=_('Numero de Telefone'),
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '+55 (55) 5555-5555 (opcional)',
            'autocomplete': 'tel'
        })
    )
    
    class Meta:
        model = User
        fields = ('email', 'name', 'company', 'phone', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Crispy forms helper for Bootstrap styling
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('email', css_class='mb-3'),
            Field('name', css_class='mb-3'),
            Row(
                Column('company', css_class='mb-3'),
                Column('phone', css_class='mb-3'),
                css_class='row'
            ),
            Field('password1', css_class='mb-3'),
            Field('password2', css_class='mb-3'),
            Submit('submit', 'Create Account', css_class='btn btn-primary btn-lg w-100')
        )
        
        # Customize password field labels and help text
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = 'Must be at least 8 characters'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = ''
    
    def clean_email(self):
        """Validate that email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('A user with this email already exists.')
            )
        return email.lower()  # Store email in lowercase
    
    def save(self, commit=True):
        """Save user with is_verified=False (will be verified via email later)"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.is_verified = False  # User needs to verify email
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Custom login form using email instead of username.
    """
    
    username = forms.EmailField(
        label=_('Email Address'),
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com',
            'autocomplete': 'email',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='mb-3'),
            Field('password', css_class='mb-3'),
            Submit('submit', 'Login', css_class='btn btn-primary btn-lg w-100')
        )