from django.contrib import admin
from .models import Contato
# Register your models here.
admin.site.site_header = 'MyApp Admin'
admin.site.index_title = 'Welcome to MyApp Admin'
admin.site.site_title = 'MyApp Admin Portal'

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'mensagem')
    search_fields = ('nome', 'email')
    list_filter = ('nome', 'email')
    ordering = ('nome',)


