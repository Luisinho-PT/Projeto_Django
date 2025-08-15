from django import forms
from .models import Contato

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'telefone', 'email', 'mensagem']
        widgets = {
            'mensagem': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        labels = {
            'nome': 'Nome',
            'telefone': 'Telefone',
            'email': 'Email',
            'mensagem': 'Mensagem',
        }