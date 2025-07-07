from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LivroForm
from .models import Livro
from django.http import JsonResponse
from django.views.decorators.http import require_GET

# Create your views here.

def index(request):
    return render(request, 'index.html')

def sobre_mim(request):
    return render(request, 'sobre_mim.html')

def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # ou redirecionar para uma página de sucesso
    else:
        form = LivroForm()
    return render(request, 'cadastrar_livro.html', {'form': form})

def livros(request):
    from .models import Livro
    livros = Livro.objects.all()
    return render(request, 'livros.html', {'livros': livros})

@require_GET
def autocomplete_livros(request):
    q = request.GET.get('q', '')
    livros = []
    if q:
        livros = Livro.objects.filter(titulo__icontains=q).values('id', 'titulo')[:10]
    return JsonResponse(list(livros), safe=False)

def listar_livros(request):
    q = request.GET.get('q', '')

    if q:
        livros = Livro.objects.filter(titulo__icontains=q)
    else:
        livros = Livro.objects.all()

    # Extraia títulos para uma lista comum (não QuerySet)
    livros_titulos = list(livros.values_list('titulo', flat=True))

    return render(request, 'livros.html', {
        'livros': livros,
        'livros_titulos': livros_titulos,
    })


def detalhe_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    return render(request, 'detalhe_livro.html', {'livro': livro})