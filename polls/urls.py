from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'),
    path('sobre_mim/', views.sobre_mim, name='sobre_mim'),
    path('', views.index, name='index'),
]
