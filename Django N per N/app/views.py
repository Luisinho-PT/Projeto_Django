# app/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Publicacao, Artigo

def gerenciar_itens_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "criar_publicacao":
            titulo = request.POST.get("titulo")
            if titulo:
                # A MÁGICA ACONTECE AQUI:
                # Tenta buscar uma Publicacao com este título. Se não existir, cria.
                obj, created = Publicacao.objects.get_or_create(
                    titulo=titulo
                )
                if created:
                    messages.success(request, f"Publicação '{titulo}' criada com sucesso!")
                else:
                    messages.info(request, f"Publicação '{titulo}' já existia no sistema.")
            else:
                messages.error(request, "O título da publicação não pode estar vazio.")
            return redirect('gerenciar_itens')

        elif action == "criar_artigo":
            titulo = request.POST.get("titulo")
            descricao = request.POST.get("descricao")
            publicacoes_ids = request.POST.getlist("publicacoes")

            if titulo and descricao and publicacoes_ids:
                # AQUI TAMBÉM:
                # Busca pelo título, se não existir, cria com os 'defaults'.
                artigo, created = Artigo.objects.get_or_create(
                    titulo=titulo,
                    defaults={'descricao': descricao}
                )

                # Independentemente de ter sido criado ou não, atualizamos as publicações.
                artigo.publicacoes.set(publicacoes_ids)

                if created:
                    messages.success(request, f"Artigo '{titulo}' criado e associado com sucesso!")
                else:
                    messages.info(request, f"Artigo '{titulo}' já existia. Suas publicações foram atualizadas.")
            else:
                messages.error(request, "Todos os campos do artigo são obrigatórios.")
            return redirect('gerenciar_itens')

    publicacoes = Publicacao.objects.all()
    context = {
        'publicacoes': publicacoes
    }
    return render(request, 'criar_artigo_e_publicacao.html', context)

def criar_artigo(request):
    publicacoes = Publicacao.objects.all()
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        publicacoes_ids = request.POST.getlist('publicacoes')  # lista de IDs selecionados

        if titulo and descricao:
            artigo = Artigo.objects.create(titulo=titulo, descricao=descricao)
            if publicacoes_ids:
                artigo.publicacao.set(publicacoes_ids)
            return redirect('criar_artigo')  # redireciona para a mesma página (ou para onde preferir)

    return render(request, 'criar_artigo_e_publicacao.html', {'publicacoes': publicacoes})

def criar_publicacao(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        if titulo:
            Publicacao.objects.create(titulo=titulo)
        return redirect('criar_artigo')  # redireciona para página de criação do artigo/publicação
    else:
        return redirect('criar_artigo')  # evita erro se acessar direto via GET