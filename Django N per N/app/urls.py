# seu_app/urls.py

from django.contrib import admin
from django.urls import path
# 1. Importa apenas a view que estamos usando
from .views import gerenciar_itens_view

urlpatterns = [
    # 2. Uma única URL para exibir a página e receber os dados dos formulários
    path('', gerenciar_itens_view, name='gerenciar_itens'),

    # Rota do painel de administração (mantida como está)
    path('admin/', admin.site.urls),
]

# 3. As URLs antigas foram removidas pois a view 'gerenciar_itens_view' agora cuida de tudo.
# path('criar-publicacao/', criar_publicacao_view, name='criar_publicacao'),
# path('criar_artigo/', criar_artigo_view, name='criar_artigo'),