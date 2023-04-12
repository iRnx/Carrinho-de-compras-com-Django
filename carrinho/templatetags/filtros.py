from django.template import Library

register = Library()

@register.filter
def qtd_carrinho(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])