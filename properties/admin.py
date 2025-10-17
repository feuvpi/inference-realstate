from django.contrib import admin
from django.utils.html import format_html
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """Admin interface for Property model"""
    
    # List view configuration
    list_display = [
        'name',
        'property_type',
        'get_location',
        'price_per_sqm',
        'total_area',
        'role_badge',
        'data_quality',
        'user',
        'created_at'
    ]
    
    list_filter = [
        'property_type',
        'is_subject',
        'is_observed',
        'data_quality',
        'city',
        'state',
        'created_at'
    ]
    
    search_fields = [
        'name',
        'street_address',
        'city',
        'neighborhood',
        'description',
        'user__email',
        'user__name'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    # Fieldsets for detail/edit view
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'property_type', 'description')
        }),
        ('Location', {
            'fields': (
                'street_address',
                'neighborhood',
                'city',
                'state',
                'zip_code',
                'country',
                ('latitude', 'longitude')
            )
        }),
        ('Market Data', {
            'fields': (
                'price_per_sqm',
                'total_price',
                'total_area',
                'transaction_date'
            ),
            'description': 'Market transaction data (for comparable properties)'
        }),
        ('Valuation Role', {
            'fields': (
                'is_subject',
                'is_observed'
            ),
            'description': 'Define how this property is used in valuation models'
        }),
        ('Data Quality', {
            'fields': (
                'data_source',
                'data_quality'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    # Custom display methods
    def get_location(self, obj):
        """Display city and neighborhood"""
        if obj.neighborhood:
            return f"{obj.neighborhood}, {obj.city}"
        return obj.city
    get_location.short_description = 'Location'
    
    def role_badge(self, obj):
        """Display property role with colored badge"""
        if obj.is_subject:
            return format_html(
                '<span style="background-color: #ffc107; color: white; '
                'padding: 3px 10px; border-radius: 3px; font-size: 11px;">'
                'SUBJECT</span>'
            )
        elif obj.is_observed:
            return format_html(
                '<span style="background-color: #28a745; color: white; '
                'padding: 3px 10px; border-radius: 3px; font-size: 11px;">'
                'COMPARABLE</span>'
            )
        return format_html(
            '<span style="background-color: #6c757d; color: white; '
            'padding: 3px 10px; border-radius: 3px; font-size: 11px;">'
            'DATA</span>'
        )
    role_badge.short_description = 'Role'
    
    # Filters
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('user')
    
    # Actions
    actions = ['mark_as_subject', 'mark_as_comparable', 'mark_high_quality']
    
    def mark_as_subject(self, request, queryset):
        """Mark selected properties as subject properties"""
        updated = queryset.update(is_subject=True, is_observed=False)
        self.message_user(request, f'{updated} properties marked as subject.')
    mark_as_subject.short_description = "Mark as subject property"
    
    def mark_as_comparable(self, request, queryset):
        """Mark selected properties as comparables"""
        updated = queryset.update(is_subject=False, is_observed=True)
        self.message_user(request, f'{updated} properties marked as comparable.')
    mark_as_comparable.short_description = "Mark as comparable property"
    
    def mark_high_quality(self, request, queryset):
        """Mark selected properties as high quality data"""
        updated = queryset.update(data_quality='high')
        self.message_user(request, f'{updated} properties marked as high quality.')
    mark_high_quality.short_description = "Mark as high quality data"