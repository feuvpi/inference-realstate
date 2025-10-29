from django.db import models
from django.core.exceptions import ValidationError


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