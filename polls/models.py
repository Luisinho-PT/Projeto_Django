from django.db import models

# Create your models here.

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    autor = models.CharField(max_length=100)
    data_publicacao = models.DateField()
    editora = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo
