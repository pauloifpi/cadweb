from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages

def index(request):
    return render(request, 'index.html')


def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id')
    }
    return render(request, 'categoria/lista.html', contexto)


def form_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request, "Operação realizada com sucesso!")

        return redirect('categoria')
    else:
        form = CategoriaForm()

    contexto = {
        'form': form,
    }
    return render(request, 'categoria/formulario.html', contexto)


def editar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')  # Redireciona para a listagem


    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('categoria')
    else:
        form = CategoriaForm(instance=categoria)

    
    return render(request, 'categoria/formulario.html', {'form': form})


def detalhes_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})

def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')  # Redireciona para a listagem

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Registro removido com sucesso.')
        return redirect('categoria')

    return render(request, 'categoria/confirmar_exclusao.html', {
        'categoria': categoria
    })
