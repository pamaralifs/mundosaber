from django.db import models

# Create your models here.
class NivelEscolar(models.Model):
    nome = models.CharField(max_length=30,verbose_name='Nome',unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Nível Escolar'
        verbose_name_plural = "Níveis Escolares"