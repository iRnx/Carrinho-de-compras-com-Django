from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detalhe_produto/<int:id>/', views.detalhe_produto, name='detalhe_produto'),
    path('adicionar_ao_carrinho/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('ver_carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('remover_carrinho/', views.remover_carrinho, name='remover_carrinho'),

]