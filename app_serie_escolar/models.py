from django.db import models
from app_nivel_escolar.models import NivelEscolar

# Create your models here.
class SerieEscolar(models.Model):
    nome = models.CharField(max_length=30,verbose_name='Nome',unique=True)
    nivel_escolar = models.ForeignKey(NivelEscolar,on_delete=models.PROTECT,related_name='series',verbose_name='Nível')

    def __str__(self):
        return self.nome + ' (' + str(self.nivel_escolar) + ')'

    class Meta:
        verbose_name = 'Série Escolar'
        verbose_name_plural = "Séries Escolares"
