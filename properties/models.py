from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Variable(models.Model):
    """
    Catálogo global de variáveis para modelos de avaliação.
    
    Define as características (variáveis independentes) que podem ser
    coletadas para cada imóvel e usadas nos modelos de regressão linear.
    
    Exemplo: área total, número de quartos, idade do imóvel, etc.
    """
    
    # Tipos de dados suportados
    DATA_TYPE_CHOICES = [
        ('decimal', 'Decimal (números com casas decimais)'),
        ('integer', 'Inteiro (números inteiros)'),
        ('boolean', 'Sim/Não (verdadeiro/falso)'),
        ('text', 'Texto (texto livre)'),
        ('choice', 'Escolha (opções pré-definidas)'),
        ('date', 'Data'),
        ('dicotomica', 'Dicotômica/Dummy (0 ou 1)'),  # Novo!
    ]
    
    # Categorias de variáveis (para organização)
    CATEGORY_CHOICES = [
        ('physical', 'Características Físicas'),
        ('location', 'Localização'),
        ('quality', 'Qualidade e Acabamento'),
        ('legal', 'Aspectos Legais'),
        ('economic', 'Aspectos Econômicos'),
        ('temporal', 'Aspectos Temporais'),
        ('proxy', 'Variáveis Proxy'),  # Novo!
        ('dicotomica', 'Variáveis Dicotômicas'),  # Novo!
        ('other', 'Outras'),
    ]
    
    # Identificação
    code = models.CharField(
        'código',
        max_length=50,
        unique=True,
        help_text='Código único para identificar a variável (ex: area_total, quartos)'
    )
    
    name = models.CharField(
        'nome',
        max_length=200,
        help_text='Nome descritivo da variável em português'
    )
    
    description = models.TextField(
        'descrição',
        blank=True,
        help_text='Descrição detalhada da variável e como medi-la'
    )
    
    category = models.CharField(
        'categoria',
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='physical',
        help_text='Categoria para organização das variáveis'
    )
    
    # Tipo de dado
    data_type = models.CharField(
        'tipo de dado',
        max_length=20,
        choices=DATA_TYPE_CHOICES,
        help_text='Tipo de dado que esta variável aceita'
    )
    
    unit = models.CharField(
        'unidade',
        max_length=20,
        blank=True,
        help_text='Unidade de medida (m², anos, unidades, etc.)'
    )
    
    # Validações para tipos numéricos
    min_value = models.DecimalField(
        'valor mínimo',
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Valor mínimo permitido (para dados numéricos)'
    )
    
    max_value = models.DecimalField(
        'valor máximo',
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Valor máximo permitido (para dados numéricos)'
    )
    
    # Opções para tipo 'choice'
    choices = models.JSONField(
        'opções',
        null=True,
        blank=True,
        help_text='Lista de opções válidas para variáveis do tipo escolha. Ex: ["Baixo", "Médio", "Alto"]'
    )
    
    # Metadados
    is_required = models.BooleanField(
        'obrigatória',
        default=False,
        help_text='Se marcado, esta variável deve ser preenchida para todos os imóveis'
    )
    
    is_active = models.BooleanField(
        'ativa',
        default=True,
        help_text='Se desmarcado, esta variável não aparecerá para uso'
    )
    
    display_order = models.IntegerField(
        'ordem de exibição',
        default=0,
        help_text='Ordem em que esta variável aparece nos formulários'
    )
    
    # Uso em modelos estatísticos
    use_in_regression = models.BooleanField(
        'usar em regressão',
        default=True,
        help_text='Se esta variável deve ser considerada nos modelos de regressão'
    )
    
    # Variáveis relacionadas (para dicotômicas e transformações)
    parent_variable = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='derived_variables',
        verbose_name='variável origem',
        help_text='Para variáveis dicotômicas: qual variável categórica originou esta'
    )
    
    transformation_rule = models.TextField(
        'regra de transformação',
        blank=True,
        help_text='Como esta variável é calculada/transformada (ex: "log(area)", "1 se padrao=Alto, 0 caso contrário")'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'variável'
        verbose_name_plural = 'variáveis'
        ordering = ['category', 'display_order', 'name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def clean(self):
        """Validação customizada"""
        from django.core.exceptions import ValidationError
        
        # Validar que choices existe para tipo 'choice'
        if self.data_type == 'choice' and not self.choices:
            raise ValidationError({
                'choices': 'Variáveis do tipo "Escolha" devem ter opções definidas.'
            })
        
        # Validar que min <= max
        if self.min_value is not None and self.max_value is not None:
            if self.min_value > self.max_value:
                raise ValidationError({
                    'max_value': 'O valor máximo deve ser maior que o valor mínimo.'
                })
        
        # Limpar choices se não for tipo 'choice'
        if self.data_type != 'choice':
            self.choices = None
    
    def get_validation_rules(self):
        """Retorna regras de validação em formato dict"""
        rules = {
            'type': self.data_type,
            'required': self.is_required,
        }
        
        if self.data_type in ['decimal', 'integer']:
            if self.min_value is not None:
                rules['min'] = float(self.min_value)
            if self.max_value is not None:
                rules['max'] = float(self.max_value)
        
        if self.data_type == 'choice' and self.choices:
            rules['choices'] = self.choices
        
        return rules
    """
    Catálogo global de variáveis para modelos de avaliação.
    
    Define as características que podem ser coletadas das propriedades
    e utilizadas nos modelos de inferência estatística (NBR 14653).
    
    Compatível com o sistema SisDea.
    """
    
    # Tipos de dados (baseado em SisDea)
    DATA_TYPE_CHOICES = [
        ('quantitativa', 'Quantitativa (Numérica)'),
        ('qualitativa_ordinal', 'Qualitativa Ordinal (Categorias Ordenadas)'),
        ('qualitativa_nominal', 'Qualitativa Nominal (Categorias)'),
    ]
    
    # Informações básicas
    code = models.CharField(
        'código',
        max_length=50,
        unique=True,
        help_text='Código único da variável (ex: area_total, quartos, padrao)'
    )
    
    name = models.CharField(
        'nome',
        max_length=200,
        help_text='Nome descritivo da variável'
    )
    
    description = models.TextField(
        'descrição',
        blank=True,
        help_text='Descrição detalhada da variável e como coletá-la'
    )
    
    # Tipo de dado
    data_type = models.CharField(
        'tipo de dado',
        max_length=25,
        choices=DATA_TYPE_CHOICES,
        help_text='Tipo de variável para análise estatística'
    )
    
    # Unidade (para variáveis quantitativas)
    unit = models.CharField(
        'unidade',
        max_length=20,
        blank=True,
        help_text='Unidade de medida (m², anos, km, R$, etc.)'
    )
    
    # Restrições para variáveis quantitativas
    min_value = models.DecimalField(
        'valor mínimo',
        max_digits=15,
        decimal_places=4,
        null=True,
        blank=True,
        help_text='Valor mínimo permitido (para quantitativas)'
    )
    
    max_value = models.DecimalField(
        'valor máximo',
        max_digits=15,
        decimal_places=4,
        null=True,
        blank=True,
        help_text='Valor máximo permitido (para quantitativas)'
    )
    
    # Opções para variáveis qualitativas
    choices = models.JSONField(
        'opções',
        null=True,
        blank=True,
        help_text='Opções para variáveis qualitativas (JSON: {"codigo": "descrição", ...})'
    )
    
    # Ordem das opções (para ordinais)
    choice_order = models.JSONField(
        'ordem das opções',
        null=True,
        blank=True,
        help_text='Ordem das opções para variáveis ordinais (JSON: ["codigo1", "codigo2", ...])'
    )
    
    # Configurações
    is_required = models.BooleanField(
        'obrigatória',
        default=False,
        help_text='Se marcado, esta variável deve ser preenchida para todos os dados'
    )
    
    is_active = models.BooleanField(
        'ativa',
        default=True,
        help_text='Se desmarcado, a variável não aparece para seleção'
    )
    
    # Metadados
    category = models.CharField(
        'categoria',
        max_length=50,
        blank=True,
        choices=[
            ('dimensoes', 'Dimensões e Áreas'),
            ('localizacao', 'Localização'),
            ('caracteristicas', 'Características Construtivas'),
            ('infraestrutura', 'Infraestrutura'),
            ('conservacao', 'Estado de Conservação'),
            ('economicas', 'Características Econômicas'),
            ('outras', 'Outras'),
        ],
        help_text='Categoria para organização'
    )
    
    created_at = models.DateTimeField(
        'criado em',
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        'atualizado em',
        auto_now=True
    )
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_choices_display(self):
        """Retorna as opções formatadas para exibição"""
        if not self.choices:
            return "N/A"
        
        if self.data_type == 'qualitativa_ordinal' and self.choice_order:
            # Ordenar pelas opções definidas
            return ', '.join([
                f"{code}: {self.choices[code]}"
                for code in self.choice_order
            ])
        else:
            # Ordem alfabética
            return ', '.join([
                f"{code}: {desc}"
                for code, desc in sorted(self.choices.items())
            ])
    
    def get_type_display_short(self):
        """Retorna tipo abreviado"""
        type_map = {
            'quantitativa': 'QUANT',
            'qualitativa_ordinal': 'QUAL-ORD',
            'qualitativa_nominal': 'QUAL-NOM',
        }
        return type_map.get(self.data_type, self.data_type)

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