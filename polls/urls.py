from django.urls import path, include
from . import views

urlpatterns = [
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'),
    path('sobre_mim/', views.sobre_mim, name='sobre_mim'),
    path('', views.index, name='index'),
    path('livros/', views.listar_livros, name='livros'),
    path('livro/<int:livro_id>/', views.detalhe_livro, name='detalhe_livro'),
    path('autocomplete-livros/', views.autocomplete_livros, name='autocomplete_livros'),
]
