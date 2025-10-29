from django.contrib import admin
from django.utils.html import format_html

    """Interface administrativa para Variáveis"""
    
    list_display = [
        'code',
        'name',
        'type_badge',
        'unit',
        'category',
        'required_badge',
        'active_badge',
        'created_at'
    ]
    
    list_filter = [
        'data_type',
        'category',
        'is_required',
        'is_active',
        'created_at'
    ]
    
    search_fields = [
        'code',
        'name',
        'description'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('code', 'name', 'description', 'category')
        }),
        ('Tipo de Dado', {
            'fields': ('data_type', 'unit')
        }),
        ('Restrições (Quantitativas)', {
            'fields': ('min_value', 'max_value'),
            'classes': ('collapse',),
            'description': 'Para variáveis quantitativas'
        }),
        ('Opções (Qualitativas)', {
            'fields': ('choices', 'choice_order'),
            'classes': ('collapse',),
            'description': 'Para variáveis qualitativas. Formato JSON.'
        }),
        ('Configurações', {
            'fields': ('is_required', 'is_active')
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def type_badge(self, obj):
        """Badge colorido para tipo"""
        colors = {
            'quantitativa': '#007bff',
            'qualitativa_ordinal': '#28a745',
            'qualitativa_nominal': '#ffc107',
        }
        color = colors.get(obj.data_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 8px; border-radius: 3px; font-size: 10px;">{}</span>',
            color,
            obj.get_type_display_short()
        )
    type_badge.short_description = 'Tipo'
    
    def required_badge(self, obj):
        """Badge para obrigatória"""
        if obj.is_required:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">●</span>'
            )
        return ''
    required_badge.short_description = 'Obrig.'
    
    def active_badge(self, obj):
        """Badge para ativa"""
        if obj.is_active:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">●</span>'
            )
        return format_html(
            '<span style="color: #6c757d; font-weight: bold;">○</span>'
        )
    active_badge.short_description = 'Ativa'
    
    actions = ['activate_variables', 'deactivate_variables']
    
    def activate_variables(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} variáveis ativadas.')
    activate_variables.short_description = "Ativar variáveis selecionadas"
    
    def deactivate_variables(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} variáveis desativadas.')
    deactivate_variables.short_description = "Desativar variáveis selecionadas"