from django.db import models
from django.contrib.auth.models import User


class Lembrete(models.Model):
    VISIVEL_CHOICES = [ ('S','Sim'), ('N','Não') ]
    titulo = models.CharField(max_length=255,unique=True,verbose_name='Título')
    conteudo = models.CharField(max_length=500,verbose_name='Conteúdo')
    visivel = models.CharField(choices=VISIVEL_CHOICES,max_length=1,verbose_name='Visível',default='S')
    data_hora_cadastro = models.DateTimeField(auto_now_add=True,verbose_name='Publicado em')
    data_hora_alteracao = models.DateTimeField(auto_now=True,verbose_name='Alterado em')
    usuario = models.ForeignKey(User,on_delete=models.PROTECT,related_name='lembretes',verbose_name='Usuário',null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Lembrete'
        verbose_name_plural = "Lembretes"
        