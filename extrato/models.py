from django.db import models
from perfil.models import Conta, Categoria

class Valores(models.Model):

    choices_tipo = (
        ('E', 'Entrada'),
        ('S', 'Saida')
    )

    valor = models.FloatField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    data = models.DateField()
    conta = models.ForeignKey(Conta, on_delete=models.DO_NOTHING)
    tipo = models.CharField(max_length=1, choices=choices_tipo)

    def __str__(self):
        return self.descricao