from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Property(models.Model):
    """
    Property model for statistical valuation analysis.
    
    Stores property data for:
    - Comparable properties (market transactions)
    - Subject properties (properties being valued)
    
    Used in linear regression models following NBR 14653 or similar
    valuation standards.
    """
    
    # Property type choices
    PROPERTY_TYPE_CHOICES = [
        ('apartment', _('Apartment')),
        ('house', _('House')),
        # ('commercial', _('Commercial')),
        # ('land', _('Land')),
        # ('industrial', _('Industrial')),
        # ('rural', _('Rural')),
        # ('other', _('Other')),
    ]
    
    # Ownership and identification
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties',
        help_text=_('User who owns this property data')
    )
    
    name = models.CharField(
        _('property name'),
        max_length=255,
        help_text=_('Descriptive name or identifier for this property')
    )
    
    property_type = models.CharField(
        _('property type'),
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        default='apartment',
        help_text=_('Type of property')
    )
    
    description = models.TextField(
        _('description'),
        blank=True,
        help_text=_('Additional notes or observations about this property')
    )
    
    # Address fields (embedded)
    street_address = models.CharField(
        _('street address'),
        max_length=255,
        help_text=_('Street name and number')
    )
    
    neighborhood = models.CharField(
        _('neighborhood'),
        max_length=100,
        blank=True,
        help_text=_('Neighborhood or district')
    )
    
    city = models.CharField(
        _('city'),
        max_length=100,
        help_text=_('City name')
    )
    
    state = models.CharField(
        _('state/province'),
        max_length=100,
        help_text=_('State or province')
    )
    
    zip_code = models.CharField(
        _('postal code'),
        max_length=20,
        blank=True,
        help_text=_('Postal/ZIP code')
    )
    
    country = models.CharField(
        _('country'),
        max_length=100,
        default='Brazil',
        help_text=_('Country')
    )
    
    # Geographic coordinates (for distance calculations in models)
    latitude = models.DecimalField(
        _('latitude'),
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text=_('Latitude coordinate (for location-based analysis)')
    )
    
    longitude = models.DecimalField(
        _('longitude'),
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text=_('Longitude coordinate (for location-based analysis)')
    )
    
    # Market data (for observed/comparable properties)
    price_per_sqm = models.DecimalField(
        _('price per square meter'),
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text=_('Transaction price per square meter (R$/m² or local currency)')
    )
    
    total_price = models.DecimalField(
        _('total transaction price'),
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text=_('Total transaction price (if known)')
    )
    
    total_area = models.DecimalField(
        _('total area (m²)'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text=_('Total built area in square meters')
    )
    
    transaction_date = models.DateField(
        _('transaction date'),
        null=True,
        blank=True,
        help_text=_('Date of transaction (for market data)')
    )
    
    # Property role in valuation models
    is_subject = models.BooleanField(
        _('is subject property'),
        default=False,
        help_text=_('Mark as TRUE if this is the property being valued (target)')
    )
    
    is_observed = models.BooleanField(
        _('is observed/comparable'),
        default=True,
        help_text=_('Mark as TRUE if this is a comparable property with known price')
    )
    
    # Data source and quality
    data_source = models.CharField(
        _('data source'),
        max_length=100,
        blank=True,
        help_text=_('Source of this data (e.g., "MLS", "Public Registry", "Direct Survey")')
    )
    
    data_quality = models.CharField(
        _('data quality'),
        max_length=20,
        choices=[
            ('high', _('High - Verified transaction')),
            ('medium', _('Medium - Secondary source')),
            ('low', _('Low - Estimated/unverified')),
        ],
        default='medium',
        help_text=_('Reliability of this property data')
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('When this property was added to the system')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('Last time this property data was updated')
    )
    
    class Meta:
        verbose_name = _('property')
        verbose_name_plural = _('properties')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_subject', 'is_observed']),
            models.Index(fields=['city', 'property_type']),
        ]
    
    def __str__(self):
        role = "Subject" if self.is_subject else "Comparable"
        return f"{self.name} ({role}) - {self.city}"
    
    def get_role_display(self):
        """Return human-readable role in valuation"""
        if self.is_subject:
            return "Subject Property (Being Valued)"
        elif self.is_observed:
            return "Comparable Property (Market Data)"
        else:
            return "Property Data"
    
    def get_full_address(self):
        """Return formatted full address"""
        parts = [
            self.street_address,
            self.neighborhood,
            self.city,
            self.state,
            self.zip_code,
            self.country
        ]
        return ', '.join(filter(None, parts))
    
    def calculate_price_per_sqm(self):
        """Calculate price per sqm if total price and area are known"""
        if self.total_price and self.total_area and self.total_area > 0:
            return self.total_price / self.total_area
        return self.price_per_sqm
    
    def save(self, *args, **kwargs):
        """Auto-calculate price_per_sqm if not provided"""
        if not self.price_per_sqm and self.total_price and self.total_area:
            if self.total_area > 0:
                self.price_per_sqm = self.total_price / self.total_area
        super().save(*args, **kwargs)