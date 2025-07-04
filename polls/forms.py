from django import forms
from .models import Livro
from django.core.exceptions import ValidationError

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Título do Livro'}),
            'autor': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Nome do Autor'}),
            'isbn': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Código ISBN'}),
            'editora': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Editora'}),
            'data_publicacao': forms.DateInput(attrs={'class': 'input-date', 'type': 'date'}),
        }
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'isbn': 'ISBN',
            'editora': 'Editora',
            'data_publicacao': 'Data de Publicação',
        }
        help_texts = {
            'titulo': 'Insira o título do livro.',
            'autor': 'Insira o nome do autor.',
            'isbn': 'Insira o código ISBN do livro.',
            'editora': 'Insira o nome da editora.',
            'data_publicacao': 'Selecione a data de publicação do livro.',
        }

def clean_isbn(self):
    isbn = self.cleaned_data['isbn']
    if Livro.objects.filter(isbn=isbn).exists():
        raise ValidationError("Esse ISBN já está cadastrado.")
    return isbn
