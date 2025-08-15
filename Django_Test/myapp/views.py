from django.shortcuts import render
from .forms import ContatoForm
# Create your views here.
def home(request):
    
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContatoForm()

    return render(request, 'home.html', {'form': form})