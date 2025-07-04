from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import LivroForm

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
