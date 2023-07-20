from django.db import models
from datetime import datetime

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    #ver aula Pythonando
    def __str__(self):
        return self.categoria
    
    def total_gasto(self):
        from extrato.models import Valores
        from perfil.utils import calcula_total
        valores = Valores.objects.filter(categoria__id = self.id).filter(data__month=datetime.now().month).filter(tipo = 'S')
        return calcula_total(valores, 'valor')
    
    def calcula_percentual_gasto_por_categoria(self):
        #try para evitar o erro de divisão por zero
        try:
            return int((self.total_gasto() * 100) / self.valor_planejamento)
        except:
            return 0
    
class Conta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa Econômica'),
        ('BR', 'Bradesco')
    )

    tipo_choices = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica')
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to='icones')

    def __str__(self):
        return self.apelido
