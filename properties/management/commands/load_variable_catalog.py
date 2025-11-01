from django.core.management.base import BaseCommand
from properties.models import Variable


class Command(BaseCommand):
    help = 'Carrega catálogo inicial de variáveis (compatível com SisDea)'
    
    def handle(self, *args, **options):
        variables = [
            # === DIMENSÕES E ÁREAS ===
            {
                'code': 'area_total',
                'name': 'Área Total',
                'description': 'Área total construída do imóvel em metros quadrados',
                'data_type': 'quantitativa',
                'unit': 'm²',
                'min_value': 0,
                'max_value': 100000,
                'category': 'dimensoes',
                'is_required': True,
            },
            {
                'code': 'area_privativa',
                'name': 'Área Privativa',
                'description': 'Área privativa do imóvel (excluindo áreas comuns)',
                'data_type': 'quantitativa',
                'unit': 'm²',
                'min_value': 0,
                'max_value': 100000,
                'category': 'dimensoes',
            },
            {
                'code': 'area_terreno',
                'name': 'Área do Terreno',
                'description': 'Área total do terreno em metros quadrados',
                'data_type': 'quantitativa',
                'unit': 'm²',
                'min_value': 0,
                'max_value': 1000000,
                'category': 'dimensoes',
            },
            {
                'code': 'frente',
                'name': 'Frente',
                'description': 'Medida da frente do terreno em metros',
                'data_type': 'quantitativa',
                'unit': 'm',
                'min_value': 0,
                'max_value': 1000,
                'category': 'dimensoes',
            },
            {
                'code': 'quartos',
                'name': 'Quartos',
                'description': 'Número de quartos/dormitórios',
                'data_type': 'quantitativa',
                'unit': 'unidades',
                'min_value': 0,
                'max_value': 20,
                'category': 'caracteristicas',
            },
            {
                'code': 'suites',
                'name': 'Suítes',
                'description': 'Número de suítes',
                'data_type': 'quantitativa',
                'unit': 'unidades',
                'min_value': 0,
                'max_value': 10,
                'category': 'caracteristicas',
            },
            {
                'code': 'banheiros',
                'name': 'Banheiros',
                'description': 'Número de banheiros',
                'data_type': 'quantitativa',
                'unit': 'unidades',
                'min_value': 0,
                'max_value': 20,
                'category': 'caracteristicas',
            },
            {
                'code': 'vagas',
                'name': 'Vagas de Garagem',
                'description': 'Número de vagas de garagem',
                'data_type': 'quantitativa',
                'unit': 'unidades',
                'min_value': 0,
                'max_value': 20,
                'category': 'caracteristicas',
            },
            
            # === LOCALIZAÇÃO ===
            {
                'code': 'dist_centro',
                'name': 'Distância ao Centro',
                'description': 'Distância ao centro da cidade em quilômetros',
                'data_type': 'quantitativa',
                'unit': 'km',
                'min_value': 0,
                'max_value': 500,
                'category': 'localizacao',
            },
            {
                'code': 'dist_metro',
                'name': 'Distância ao Metrô',
                'description': 'Distância à estação de metrô mais próxima em metros',
                'data_type': 'quantitativa',
                'unit': 'm',
                'min_value': 0,
                'max_value': 50000,
                'category': 'localizacao',
            },
            
            # === CARACTERÍSTICAS CONSTRUTIVAS ===
            {
                'code': 'idade',
                'name': 'Idade Aparente',
                'description': 'Idade aparente do imóvel em anos',
                'data_type': 'quantitativa',
                'unit': 'anos',
                'min_value': 0,
                'max_value': 200,
                'category': 'caracteristicas',
            },
            {
                'code': 'andar',
                'name': 'Andar',
                'description': 'Andar do apartamento (0=térreo)',
                'data_type': 'quantitativa',
                'unit': 'unidades',
                'min_value': 0,
                'max_value': 100,
                'category': 'caracteristicas',
            },
            
            # === QUALITATIVAS ORDINAIS ===
            {
                'code': 'padrao',
                'name': 'Padrão Construtivo',
                'description': 'Padrão de acabamento e construção do imóvel',
                'data_type': 'qualitativa_ordinal',
                'choices': {
                    'baixo': 'Baixo',
                    'medio': 'Médio',
                    'alto': 'Alto',
                    'luxo': 'Luxo'
                },
                'choice_order': ['baixo', 'medio', 'alto', 'luxo'],
                'category': 'caracteristicas',
            },
            {
                'code': 'conservacao',
                'name': 'Estado de Conservação',
                'description': 'Estado geral de conservação do imóvel',
                'data_type': 'qualitativa_ordinal',
                'choices': {
                    'pessimo': 'Péssimo',
                    'ruim': 'Ruim',
                    'regular': 'Regular',
                    'bom': 'Bom',
                    'otimo': 'Ótimo',
                    'novo': 'Novo/Reformado'
                },
                'choice_order': ['pessimo', 'ruim', 'regular', 'bom', 'otimo', 'novo'],
                'category': 'conservacao',
            },
            {
                'code': 'localizacao_qualidade',
                'name': 'Qualidade da Localização',
                'description': 'Avaliação qualitativa da localização (bairro, infraestrutura)',
                'data_type': 'qualitativa_ordinal',
                'choices': {
                    'ruim': 'Ruim',
                    'regular': 'Regular',
                    'boa': 'Boa',
                    'otima': 'Ótima',
                    'excelente': 'Excelente'
                },
                'choice_order': ['ruim', 'regular', 'boa', 'otima', 'excelente'],
                'category': 'localizacao',
            },
            
            # === QUALITATIVAS NOMINAIS ===
            {
                'code': 'posicao_quadra',
                'name': 'Posição na Quadra',
                'description': 'Posição do imóvel na quadra',
                'data_type': 'qualitativa_nominal',
                'choices': {
                    'meio': 'Meio de Quadra',
                    'esquina': 'Esquina',
                    'duas_frentes': 'Duas Frentes',
                    'vila': 'Vila/Encravado'
                },
                'category': 'localizacao',
            },
            {
                'code': 'vista',
                'name': 'Vista',
                'description': 'Tipo de vista do imóvel',
                'data_type': 'qualitativa_nominal',
                'choices': {
                    'interna': 'Interna/Limitada',
                    'rua': 'Rua',
                    'lateral': 'Lateral',
                    'livre': 'Livre/Ampla',
                    'panoramica': 'Panorâmica',
                    'mar': 'Mar',
                    'montanha': 'Montanha'
                },
                'category': 'caracteristicas',
            },
            {
                'code': 'orientacao_solar',
                'name': 'Orientação Solar',
                'description': 'Orientação solar predominante',
                'data_type': 'qualitativa_nominal',
                'choices': {
                    'norte': 'Norte',
                    'sul': 'Sul',
                    'leste': 'Leste',
                    'oeste': 'Oeste',
                    'nordeste': 'Nordeste',
                    'noroeste': 'Noroeste',
                    'sudeste': 'Sudeste',
                    'sudoeste': 'Sudoeste'
                },
                'category': 'caracteristicas',
            },
            
            # === INFRAESTRUTURA (Boolean/Dummy) ===
            {
                'code': 'elevador',
                'name': 'Elevador',
                'description': 'Presença de elevador no edifício',
                'data_type': 'qualitativa_nominal',
                'choices': {
                    'nao': 'Não',
                    'sim': 'Sim'
                },
                'category': 'infraestrutura',
            },
            {
                'code': 'piscina',
                'name': 'Piscina',
                'description': 'Presença de piscina (condomínio ou privativa)',
                'data_type': 'qualitativa_nominal',
                'choices': {
                    'nao': 'Não',
                    'sim': 'Sim'
                },
                'category': 'infraestrutura',
            },
            {
                'code': 'churrasqueira',
                'name': 'Churrasqueira',
                'description': 'Presença de churrasqueira',
                'data_type': 'qualitativa_nominal',
                'choices': {
                    'nao': 'Não',
                    'sim': 'Sim'
                },
                'category': 'infraestrutura',
            },
            {
                'code': 'varanda',
                'name': 'Varanda/Sacada',
                'description': 'Presença de varanda ou sacada',
                'data_type': 'qualitativa_nominal',
                'choices': {
                    'nao': 'Não',
                    'sim': 'Sim'
                },
                'category': 'caracteristicas',
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
            else:
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Catálogo carregado com sucesso!\n'
                f'Variáveis criadas: {created_count}\n'
                f'Variáveis atualizadas: {updated_count}\n'
                f'Total: {len(variables)}'
            )
        )