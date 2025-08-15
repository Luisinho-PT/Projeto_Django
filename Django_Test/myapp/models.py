from django.db import models

# Create your models here.

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    mensagem = models.TextField()

    def __str__(self):
        return self.nome
    
class Retorno(models.Model):
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)
    resposta = models.TextField()
    data_resposta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Retorno para {self.contato.nome} em {self.data_resposta}'