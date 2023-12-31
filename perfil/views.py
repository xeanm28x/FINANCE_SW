from django.shortcuts import render, redirect
from .models import Conta, Categoria
from extrato.models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total
from datetime import datetime
from contas.views import quantificar_contas

def home(request):
    contas = Conta.objects.all()
    valores = Valores.objects.filter(data__month = datetime.now().month)
    entradas = valores.filter(tipo = 'E')
    saidas = valores.filter(tipo = 'S')

    total_contas = calcula_total(contas, 'valor')
    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')

    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()
    t_contas_vencidas, t_contas_proximas_vencimento = quantificar_contas()

    return render(request, 'home.html', {'contas': contas, 'total_contas': total_contas, 'total_entradas': total_entradas, 'total_saidas': total_saidas, 'percentual_gastos_essenciais' : int(percentual_gastos_essenciais), 'percentual_gastos_nao_essenciais' : int(percentual_gastos_nao_essenciais), 't_contas_vencidas' : t_contas_vencidas, 't_contas_proximas_vencimento' : t_contas_proximas_vencimento})

def gerenciar(request):
    contas = Conta.objects.all()
    total_contas = 0
    categorias = Categoria.objects.all()
    total_contas = calcula_total(contas, 'valor')
    return render(request, 'gerenciar.html', {'contas': contas, 'total_contas': total_contas, 'categorias': categorias})

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')
    
    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos.')
        return redirect('/perfil/gerenciar/')

    conta = Conta(
        apelido = apelido,
        banco = banco,
        tipo = tipo,
        valor = valor,
        icone = icone
    )

    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
    return redirect('/perfil/gerenciar/', {'conta': conta})

def deletar_conta(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()

    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso!')
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))
    
    if len(nome.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha o nome da categoria.')
        return redirect('/perfil/gerenciar/')

    categoria = Categoria(
        categoria = nome,
        essencial = essencial
    )

    categoria.save()
    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso!')
    return redirect('/perfil/gerenciar/')

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()
    return redirect('/perfil/gerenciar/')

def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        valores = Valores.objects.filter(categoria=categoria)
        dados[categoria.categoria] = calcula_total(valores, 'valor')

    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})

def calcula_equilibrio_financeiro():
    gastos_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False)
    total_gastos_essenciais = calcula_total(gastos_essenciais, 'valor')
    total_gastos_nao_essenciais = calcula_total(gastos_nao_essenciais, 'valor')

    total = total_gastos_essenciais + total_gastos_nao_essenciais

    try:
        percentual_gastos_essenciais = total_gastos_essenciais * 100 / total
        percentual_gastos_nao_essenciais = total_gastos_nao_essenciais * 100 / total

        return percentual_gastos_essenciais, percentual_gastos_nao_essenciais
    
    except:
        return 0, 0