from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password"""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model that uses email instead of username for authentication.
    
    This model is designed for a property valuation SaaS where users are
    typically professionals (appraisers, real estate agents) working for companies.
    """
    
    # Remove username field (we use email instead)
    username = None
    
    # Core authentication field
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. Used for login and notifications.')
    )
    
    # Personal information
    name = models.CharField(
        _('full name'),
        max_length=255,
        help_text=_('Full name of the user')
    )
    
    phone = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        help_text=_('Contact phone number (optional)')
    )
    
    # Business information
    company = models.CharField(
        _('company name'),
        max_length=255,
        blank=True,
        help_text=_('Company or organization name (optional)')
    )
    
    # Account verification
    is_verified = models.BooleanField(
        _('email verified'),
        default=False,
        help_text=_('Designates whether the user has verified their email address.')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use email for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Required when creating superuser
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the name"""
        return self.name
    
    def get_short_name(self):
        """Return the first name"""
        return self.name.split()[0] if self.name else self.email