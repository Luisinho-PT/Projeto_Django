# app/management/commands/cleanup_duplicates.py

from django.core.management.base import BaseCommand
from django.db.models import Count
from app.models import Publicacao, Artigo

class Command(BaseCommand):
    help = 'Encontra e deleta publicações e artigos duplicados, unificando as relações N-N e mantendo o mais antigo.'

    def handle(self, *args, **options):
        # A limpeza de Publicacao não precisa de tratamento especial de relações N-N
        self.cleanup_simple_model(Publicacao, 'Publicação')
        
        # A limpeza de Artigo PRECISA de tratamento especial
        self.cleanup_artigos_with_m2m()
        
        self.stdout.write(self.style.SUCCESS('Limpeza de duplicados concluída.'))

    def cleanup_simple_model(self, model, model_name):
        """Função para limpar modelos sem relações M2M para consolidar."""
        self.stdout.write(f'--- Verificando duplicados para o modelo: {model_name} ---')
        
        duplicate_titles = model.objects.values('titulo').annotate(title_count=Count('id')).filter(title_count__gt=1)

        if not duplicate_titles:
            self.stdout.write(self.style.SUCCESS(f'Nenhum duplicado encontrado para {model_name}.'))
            return

        total_deleted = 0
        for entry in duplicate_titles:
            titulo = entry['titulo']
            duplicates = model.objects.filter(titulo=titulo).order_by('id')
            original = duplicates.first()
            to_delete = duplicates.exclude(id=original.id)
            
            count_to_delete = to_delete.count()
            if count_to_delete > 0:
                self.stdout.write(f"Processando '{titulo}': Mantendo ID {original.id} e deletando {count_to_delete} duplicados.")
                to_delete.delete()
                total_deleted += count_to_delete
        
        if total_deleted > 0:
            self.stdout.write(self.style.SUCCESS(f'Total de {total_deleted} {model_name}(s) duplicados foram deletados.'))

    def cleanup_artigos_with_m2m(self):
        """Função específica para limpar Artigos, consolidando as relações M2M."""
        model_name = 'Artigo'
        self.stdout.write(f'--- Verificando duplicados para o modelo: {model_name} (com unificação de relações) ---')

        duplicate_titles = Artigo.objects.values('titulo').annotate(title_count=Count('id')).filter(title_count__gt=1)

        if not duplicate_titles:
            self.stdout.write(self.style.SUCCESS(f'Nenhum duplicado encontrado para {model_name}.'))
            return

        total_deleted = 0
        for entry in duplicate_titles:
            titulo = entry['titulo']
            duplicates = Artigo.objects.filter(titulo=titulo).order_by('id')
            
            # O primeiro da lista (o mais antigo) é o que vamos manter
            original_artigo = duplicates.first()
            
            # Os restantes são para deletar
            artigos_to_delete = duplicates.exclude(id=original_artigo.id)

            self.stdout.write(f"Processando '{titulo}': Mantendo Artigo ID {original_artigo.id}.")

            # --- PASSO CRUCIAL: UNIFICAR RELAÇÕES ---
            for artigo_duplicado in artigos_to_delete:
                # Pega todas as publicações do artigo duplicado
                publicacoes = artigo_duplicado.publicacoes.all()
                if publicacoes:
                    self.stdout.write(f"  > Movendo {publicacoes.count()} relação(ões) do Artigo duplicado ID {artigo_duplicado.id} para o original.")
                    # Adiciona essas publicações ao artigo original
                    original_artigo.publicacoes.add(*publicacoes)

            # Agora que as relações foram salvas, podemos deletar os duplicados
            count_to_delete = artigos_to_delete.count()
            if count_to_delete > 0:
                artigos_to_delete.delete()
                self.stdout.write(self.style.WARNING(f"  Deletados {count_to_delete} Artigos duplicados."))
                total_deleted += count_to_delete

        if total_deleted > 0:
            self.stdout.write(self.style.SUCCESS(f'Total de {total_deleted} {model_name}(s) duplicados foram deletados.'))