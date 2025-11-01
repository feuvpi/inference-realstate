from django.core.management.base import BaseCommand
from properties.models import Variable


class Command(BaseCommand):
    help = 'Carrega variáveis padrão para avaliação imobiliária (NBR 14653)'
    
    def handle(self, *args, **options):
        variables = [
            # Características Físicas
            {
                'code': 'area_total',
                'name': 'Área Total',
                'description': 'Área total construída do imóvel em metros quadrados',
                'category': 'physical',
                'data_type': 'decimal',
                'unit': 'm²',
                'min_value': 0,
                'max_value': 10000,
                'is_required': True,
                'use_in_regression': True,
                'display_order': 10
            },
            {
                'code': 'area_privativa',
                'name': 'Área Privativa',
                'description': 'Área privativa do imóvel (sem áreas comuns)',
                'category': 'physical',
                'data_type': 'decimal',
                'unit': 'm²',
                'min_value': 0,
                'max_value': 10000,
                'is_required': False,
                'use_in_regression': True,
                'display_order': 11
            },
            {
                'code': 'area_terreno',
                'name': 'Área do Terreno',
                'description': 'Área total do terreno (para casas)',
                'category': 'physical',
                'data_type': 'decimal',
                'unit': 'm²',
                'min_value': 0,
                'max_value': 100000,
                'is_required': False,
                'use_in_regression': True,
                'display_order': 12
            },
            {
                'code': 'testada',
                'name': 'Testada',
                'description': 'Medida da frente do terreno',
                'category': 'physical',
                'data_type': 'decimal',
                'unit': 'm',
                'min_value': 0,
                'max_value': 1000,
                'is_required': False,
                'use_in_regression': True,
                'display_order': 13
            },
            {
                'code': 'topografia',
                'name': 'Topografia',
                'description': 'Característica topográfica do terreno',
                'category': 'physical',
                'data_type': 'choice',
                'unit': '',
                'choices': ['Plano', 'Aclive', 'Declive', 'Irregular'],
                'is_required': False,
                'use_in_regression': True,
                'display_order': 14
            },
            {
                'code': 'quartos',
                'name': 'Número de Quartos',
                'description': 'Quantidade de quartos/dormitórios',
                'category': 'physical',
                'data_type': 'integer',
                'unit': 'unidades',
                'min_value': 0,
                'max_value': 20,
                'is_required': False,
                'use_in_regression': True,
                'display_order': 20
            },
            {
                'code': 'suites',
                'name': 'Número de Suítes',
                'description': 'Quantidade de suítes (quartos com banheiro)',
                'category': 'physical',
                'data_type': 'integer',
                'unit': 'unidades',
                'min_value': 0,
                'max_value': 10,
                'is_required': False,
                'use_in_regression': True,
                'display_order': 21
            },
            {
                'code': 'banheiros',
                'name': 'Número de Banheiros',
                'description': 'Quantidade total de banheiros',
                'category': 'physical',
                'data_type': 'integer',
                'unit': 'unidades',
                'min_value': 0,
                'max_value': 10,
                'is_required': False,
                'use_in_regression': True,
                'display_order': 22
            },
            {
                'code': 'vagas_garagem',
                'name': 'Vagas de Garagem',
                'description': 'Número de vagas de garagem',
                'category': 'physical',
                'data_type': 'integer',
                'unit': 'vagas',
                'min_value': 0,
                'max_value': 10,
                'is_required': False,
                'use_in_regression': True,
                'display_order': 30
            },
            {
                'code': 'andar',
                'name': 'Andar',
                'description': 'Andar do imóvel (para apartamentos)',
                'category': 'physical',
                'data_type': 'integer',
                'unit': 'andar',
                'min_value': 0,
                'max_value': 100,
                'is_required': False,
                'use_in_regression': True,
                'display_order': 31
            },
            {
                'code': 'elevador',
                'name': 'Possui Elevador',
                'description': 'Indica se o prédio possui elevador',
                'category': 'physical',
                'data_type': 'boolean',
                'unit': '',
                'is_required': False,
                'use_in_regression': True,
                'display_order': 70
            },
            {
                'code': 'piscina',
                'name': 'Possui Piscina',
                'description': 'Indica se possui piscina (privativa ou condomínio)',
                'category': 'physical',
                'data_type': 'boolean',
                'unit': '',
                'is_required': False,
                'use_in_regression': True,
                'display_order': 71
            },
            
            # Qualidade e Acabamento
            {
                'code': 'padrao_construcao',
                'name': 'Padrão de Construção',
                'description': 'Padrão construtivo e acabamento do imóvel',
                'category': 'quality',
                'data_type': 'choice',
                'unit': '',
                'choices': ['Baixo', 'Normal', 'Alto', 'Luxo'],
                'is_required': False,
                'use_in_regression': True,
                'display_order': 50
            },
            {
                'code': 'estado_conservacao',
                'name': 'Estado de Conservação',
                'description': 'Estado atual de conservação do imóvel',
                'category': 'quality',
                'data_type': 'choice',
                'unit': '',
                'choices': ['Ruim', 'Regular', 'Bom', 'Ótimo', 'Novo'],
                'is_required': False,
                'use_in_regression': True,
                'display_order': 51
            },
            {
                'code': 'portaria_24h',
                'name': 'Portaria 24h',
                'description': 'Indica se possui portaria 24 horas',
                'category': 'quality',
                'data_type': 'boolean',
                'unit': '',
                'is_required': False,
                'use_in_regression': True,
                'display_order': 72
            },
            
            # Localização
            {
                'code': 'distancia_centro',
                'name': 'Distância ao Centro',
                'description': 'Distância aproximada ao centro da cidade',
                'category': 'location',
                'data_type': 'decimal',
                'unit': 'km',
                'min_value': 0,
                'max_value': 100,
                'is_required': False,
                'use_in_regression': True,
                'display_order': 60
            },
            {
                'code': 'vista',
                'name': 'Vista',
                'description': 'Tipo de vista do imóvel',
                'category': 'location',
                'data_type': 'choice',
                'unit': '',
                'choices': ['Sem vista', 'Vista parcial', 'Vista livre', 'Vista mar/lago'],
                'is_required': False,
                'use_in_regression': True,
                'display_order': 61
            },
            {
                'code': 'frente',
                'name': 'Frente',
                'description': 'Posicionamento do imóvel (frente/fundos)',
                'category': 'location',
                'data_type': 'choice',
                'unit': '',
                'choices': ['Frente', 'Fundos', 'Lateral'],
                'is_required': False,
                'use_in_regression': True,
                'display_order': 62
            },
            {
                'code': 'posicao_solar',
                'name': 'Posição Solar',
                'description': 'Orientação solar do imóvel',
                'category': 'location',
                'data_type': 'choice',
                'unit': '',
                'choices': ['Norte', 'Sul', 'Leste', 'Oeste', 'Nordeste', 'Noroeste', 'Sudeste', 'Sudoeste'],
                'is_required': False,
                'use_in_regression': True,
                'display_order': 63
            },
            
            # Aspectos Temporais
            {
                'code': 'idade_imovel',
                'name': 'Idade do Imóvel',
                'description': 'Idade aproximada do imóvel em anos',
                'category': 'temporal',
                'data_type': 'integer',
                'unit': 'anos',
                'min_value': 0,
                'max_value': 200,
                'is_required': False,
                'use_in_regression': True,
                'display_order': 40
            },
            
            # Variáveis Proxy
            {
                'code': 'valor_condominio',
                'name': 'Valor do Condomínio',
                'description': 'Valor mensal do condomínio (proxy para qualidade)',
                'category': 'proxy',
                'data_type': 'decimal',
                'unit': 'R$',
                'min_value': 0,
                'max_value': 50000,
                'is_required': False,
                'use_in_regression': True,
                'display_order': 80
            },
            {
                'code': 'iptu_anual',
                'name': 'IPTU Anual',
                'description': 'Valor do IPTU anual (proxy para valor venal)',
                'category': 'proxy',
                'data_type': 'decimal',
                'unit': 'R$',
                'min_value': 0,
                'max_value': 100000,
                'is_required': False,
                'use_in_regression': True,
                'display_order': 81
            },
            
            # Variáveis Dicotômicas (exemplos)
            {
                'code': 'dic_padrao_alto',
                'name': 'Dummy: Padrão Alto',
                'description': 'Variável dicotômica: 1 se padrão=Alto, 0 caso contrário',
                'category': 'dicotomica',
                'data_type': 'dicotomica',
                'unit': '',
                'is_required': False,
                'use_in_regression': True,
                'display_order': 90,
                'transformation_rule': '1 se padrao_construcao="Alto", 0 caso contrário'
            },
            {
                'code': 'dic_padrao_luxo',
                'name': 'Dummy: Padrão Luxo',
                'description': 'Variável dicotômica: 1 se padrão=Luxo, 0 caso contrário',
                'category': 'dicotomica',
                'data_type': 'dicotomica',
                'unit': '',
                'is_required': False,
                'use_in_regression': True,
                'display_order': 91,
                'transformation_rule': '1 se padrao_construcao="Luxo", 0 caso contrário'
            },
            {
                'code': 'dic_vista_mar',
                'name': 'Dummy: Vista Mar',
                'description': 'Variável dicotômica: 1 se vista=mar/lago, 0 caso contrário',
                'category': 'dicotomica',
                'data_type': 'dicotomica',
                'unit': '',
                'is_required': False,
                'use_in_regression': True,
                'display_order': 92,
                'transformation_rule': '1 se vista="Vista mar/lago", 0 caso contrário'
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for var_data in variables:
            variable, created = Variable.objects.update_or_create(
                code=var_data['code'],
                defaults=var_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Criada: {variable.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'→ Atualizada: {variable.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Processo concluído: {created_count} criadas, '
                f'{updated_count} atualizadas'
            )
        )