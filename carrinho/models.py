from django.db import models
from stdimage import StdImageField

class Produto(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    imagem = StdImageField(upload_to='imagem', variations={'thumbnail': {'width': 500, 'height': 500}})
    preco = models.FloatField()

    def __str__(self) -> str:
        return self.nome

    def formata_preco(self):
        return f'R$ {self.preco:.2f}'.replace('.', ',')
    formata_preco.short_description = 'Preço'


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    preco = models.FloatField()

    def __str__(self) -> str:
        return self.nome
   


