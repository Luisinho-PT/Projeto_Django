from django.core.management.base import BaseCommand
from polls.models import Livro
from django.db.models import Count

class Command(BaseCommand):
    help = "Remove livros duplicados pelo campo ISBN, mantendo um registro."

    def handle(self, *args, **kwargs):
        duplicados = (
            Livro.objects
            .values('isbn')
            .annotate(isbn_count=Count('isbn'))
            .filter(isbn_count__gt=1)
        )

        total_deletados = 0

        for d in duplicados:
            livros = Livro.objects.filter(isbn=d['isbn']).order_by('id')
            primeiro = livros.first()  # mantém o primeiro registro

            for livro in livros[1:]:
                livro.delete()
                total_deletados += 1
                self.stdout.write(f"Livro duplicado deletado: ID {livro.id} ISBN {livro.isbn}")

        self.stdout.write(self.style.SUCCESS(f"Limpeza concluída. {total_deletados} registros duplicados deletados."))
        if total_deletados == 0:
            self.stdout.write(self.style.SUCCESS("Nenhum registro duplicado encontrado."))
        else:
            self.stdout.write(self.style.SUCCESS(f"{total_deletados} registros duplicados foram removidos."))