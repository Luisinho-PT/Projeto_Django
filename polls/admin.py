from django.contrib import admin
# Register your models here.

from polls.models import Livro

class LivroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'isbn', 'data_publicacao')
    search_fields = ('titulo', 'autor', 'isbn')
    list_filter = ('data_publicacao',)

admin.site.register(Livro, LivroAdmin)
admin.site.site_header = "Administração de Livros"
admin.site.site_title = "Administração de Livros"
admin.site.index_title = "Bem-vindo à administração de livros"
# Customizando o título do site de administração

