from django.shortcuts import render, redirect
from perfil.models import Conta, Categoria
from .models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse, FileResponse
from datetime import datetime
from django.template.loader import render_to_string
import os
from django.conf import settings
from weasyprint import HTML
from io import BytesIO

def novo_valor(request):

    if request.method == 'GET':

        contas = Conta.objects.all()
        categorias = Categoria.objects.all()

        return render(request, 'novo_valor.html', {'contas': contas, 'categorias': categorias})
    
    elif request.method == 'POST':

        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')

        valores = Valores(
            valor = valor,
            categoria_id = categoria,
            descricao = descricao,
            data = data,
            conta_id = conta,
            tipo = tipo
        )

        valores.save()

        #pega os id's e compara para encontrar a correta
        #id = id da tabela conta
        #conta = variavel contendo a conta do formulário
        
        conta = Conta.objects.get(id = conta)

        if tipo == 'E':
            conta.valor += int(valor)
            messages.add_message(request, constants.SUCCESS, 'Entrada cadastrada com sucesso!')
        else:
            conta.valor -= int(valor)
            messages.add_message(request, constants.SUCCESS, 'Saída cadastrada com sucesso!')
        
        conta.save()
        return redirect('/extrato/novo_valor/')
    
def view_extrato(request):

    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    valores = Valores.objects.filter(data__month = datetime.now().month)
    conta_filtro = request.GET.get('conta')
    categoria_filtro = request.GET.get('categoria')

    if conta_filtro and categoria_filtro:
        valores = valores.filter(conta__id = conta_filtro)
        valores = valores.filter(categoria__id = categoria_filtro)

    valores = valores.filter()
    
    #to do: filtro por periodo

    return render(request, 'view_extrato.html', {'contas': contas, 'categorias': categorias, 'valores': valores})

def exportar_pdf(request):

    valores = Valores.objects.filter(data__month = datetime.now().month)
    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    template_render = render_to_string(path_template, {'valores': valores})
    path_output = BytesIO()

    HTML(string=template_render).write_pdf(path_output)

    path_output.seek(0)

    return FileResponse(path_output, filename="extrato.pdf")