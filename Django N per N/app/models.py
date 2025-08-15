from django.db import models

# Create your models here.


class Publicacao(models.Model):
    titulo = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo

class Artigo(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    publicacoes = models.ManyToManyField(Publicacao, related_name='artigos')

    def __str__(self):
        return self.titulo
