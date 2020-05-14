from django.db import models

# Create your models here.
class Acesso(models.Model):
    ip_cliente = models.CharField(null=True,max_length=50,verbose_name='REMOTE_ADDR')
    ip_cliente_x_forwarded_primeiro = models.CharField(null=True,max_length=50,verbose_name='REMOTE_X_FORWARDED_FOR_PRIMEIRO')
    ip_cliente_x_forwarded_ultimo = models.CharField(null=True,max_length=50,verbose_name='REMOTE_X_FORWARDED_FOR_ULTIMO')
    host_cliente = models.CharField(null=True,max_length=255,verbose_name='HTTP_HOST')
    agente_cliente_navegador = models.CharField(null=True,max_length=255,verbose_name='HTTP_USER_AGENT')
    data_hora_acesso = models.DateTimeField(auto_now_add=True,null=True,verbose_name='DATA HORA ACESSO')

    def __str__(self):
        return 'Acessado por: {0} - Em: {1}'.format(self.ip_cliente,self.data_hora_acesso,agente_cliente_navegador)

    class Meta:
        verbose_name = 'Acesso'
        verbose_name_plural = 'Acessos'

#https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META
#HttpRequest.META
#HTTP_HOST - O cabeçalho do host HTTP enviado pelo cliente.
#HTTP_USER_AGENT - A sequência de agente do usuário do cliente.
#REMOTE_ADDR - O endereço IP do cliente.
#No metodo
#def save_model(self, request, obj, form, change):
#    obj.ip = request.META['REMOTE_ADDR']
#    obj.save()
#MELHOR
#https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
#Dizem que no caso de proxy (forwarded) o ip externo do clinte é o mais à direita (último da string/lista)
#    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#    if x_forwarded_for:
#    ip = x_forwarded_for.split(',')[0].strip()
#        ip = x_forwarded_for.split(',')[-1].strip()
#    ip = request.META.get('REMOTE_ADDR', None)
#
#https://groups.google.com/forum/#!topic/django-brasil/Ap9D3fG0G-4
# request.META['REMOTE_ADDR'] e request.META['HTTP_USER_AGENT'].

