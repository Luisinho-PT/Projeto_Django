from django.core.management.base import BaseCommand
from polls.models import Livro
from django.db.models import Count

class Command(BaseCommand):
    help = "Deleta livros usando o ISBN"
    def handle(self, *args, **kwargs):
        isbn = input("Digite o ISBN do livro a ser deletado: ")
        try:
            livro = Livro.objects.get(isbn=isbn)
            livro.delete()
            self.stdout.write(self.style.SUCCESS(f"Livro com ISBN {isbn} deletado com sucesso."))
        except Livro.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Nenhum livro encontrado com o ISBN {isbn}."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocorreu um erro ao tentar deletar o livro: {str(e)}"))
