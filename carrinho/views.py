from pprint import pprint
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Produto, Variacao
from django.contrib import messages


def home(request):
    
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos': produtos})


def detalhe_produto(request, id):

    produto = get_object_or_404(Produto, id=id)
    return render(request, 'detalhe_produto.html', {'produto': produto})


def adicionar_carrinho(request):

    if not request.session.get('carrinho'):
        request.session['carrinho'] = {}
        request.session.save()

    variacao_id = request.GET.get('vid')
    variacao = get_object_or_404(Variacao, id=variacao_id)

    if variacao_id in request.session['carrinho']:
        quantidade = request.session['carrinho'][variacao_id]['quantidade']
        quantidade += 1
        request.session['carrinho'][variacao_id]['quantidade'] = quantidade
        request.session['carrinho'][variacao_id]['preco'] = quantidade * variacao.produto.preco
    else:
        request.session['carrinho'][variacao_id] = {
                'quantidade': 1,
                'imagem': variacao.produto.imagem.url,
                'variacao_id': variacao_id,
                'variacao_nome': variacao.nome,
                'nome': variacao.produto.nome,
                'preco': variacao.produto.preco,
            }
    pprint(request.session['carrinho'])
    request.session.save()

    # quantidade = sum([item['quantidade'] for item in request.session['carrinho'].values()])
    messages.success(request, f'"{variacao.produto.nome} {variacao.nome}" adicionado ao carrinho')

    return redirect(reverse('detalhe_produto', kwargs={'id': variacao.produto.id}))   


def ver_carrinho(request):
     
    try:
        dados_mostrar = []

        for item in request.session['carrinho'].values():

            dados_mostrar.append({
                'quantidade': item['quantidade'],
                'variacao_id': item['variacao_id'],
                'variacao_nome': item['variacao_nome'],
                'imagem': item['imagem'],
                'nome': item['nome'],
                'preco': f"R$ {item['preco']:.2f}",
            })

        print(dados_mostrar)
        total = sum([float(i['preco']) for i in request.session['carrinho'].values()])
    
        return render(request, 'ver_carrinho.html', {'dados': dados_mostrar, 'total': f'{total:.2f}',})
    except KeyError:
                return render(request, 'ver_carrinho.html')


def remover_carrinho(request):

    variacao_id = request.GET.get('vid')
    variacao = get_object_or_404(Variacao, id=variacao_id)

    # Remover um produto expecífico
    del request.session['carrinho'][variacao_id]
    request.session.save()

    messages.success(request, f'"{variacao.produto.nome} {variacao.nome}" removido do seu carrinho')
    return redirect('ver_carrinho')
