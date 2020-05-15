from django.shortcuts import render
from django.views.generic import View,TemplateView,ListView
from .models import Acesso
from app_lembrete.models import Lembrete

# Create your views here.

#HOME
class Home(TemplateView):  # extend from TemplateView e NÃO TEM def query_set
    template_name = 'app_core/index.html'
    ordering = ['-id'] # Ou ordeno aqui
    #template_name = 'app_lembrete/lembrete_visiveis_list.html' SERÁ VIA INCLUDE
    #paginate_by = 3

    # Métodos CBVs
    # http://pythonclub.com.br/class-based-views-django.html
    #def get_queryset(self,**kwargs):
        #queryset = super(Home, self).get_queryset()
        #queryset = queryset.filter(visivel = 'S').order_by('-id')
        #return queryset.order_by('-id')
        #print(self.model.objects._meta.verbose_name)
        #return self.model.filter(visivel = 'S').order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['now'] = datetime.now()

        #pega ip do cliente e salva no banco no primeiro acesso/home da sessão
        #https://stackoverflow.com/questions/16243560/django-detailview-how-to-use-request-in-get-context-data
        #https://docs.djangoproject.com/en/dev/topics/class-based-views/generic-display/#dynamic-filtering
        #Você tem acesso à solicitação em self.request
        obj_acesso = Acesso()
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            obj_acesso.ip_cliente_x_forwarded_primeiro = x_forwarded_for.split(',')[0].strip()
            obj_acesso.ip_cliente_x_forwarded_ultimo = x_forwarded_for.split(',')[-1].strip()
        else:
            obj_acesso.ip_cliente_x_forwarded_primeiro = None
            obj_acesso.ip_cliente_x_forwarded_ultimo = None          
        
        obj_acesso.ip_cliente = self.request.META.get('REMOTE_ADDR', None) 
        if not obj_acesso.ip_cliente and x_forwarded_for:
            obj_acesso.ip_cliente = obj_acesso.ip_cliente_x_forwarded_ultimo


        obj_acesso.host_cliente = self.request.META.get('HTTP_HOST', None) 
        obj_acesso.agente_cliente_navegador = self.request.META.get('HTTP_USER_AGENT', None) 
        obj_acesso.save()
        #Acesso(cod_usuario=user.id).save()
        #Acesso(id=???,ip_cliente,ip_cliente_x_forwarded_primeiro,ip_cliente_x_forwarded_ultimo,host_cliente,).save() precisou do id

        context['ip_cliente'] = obj_acesso.ip_cliente
        context['ip_cliente_x_forwarded_primeiro'] = obj_acesso.ip_cliente_x_forwarded_primeiro
        context['ip_cliente_x_forwarded_ultimo'] = obj_acesso.ip_cliente_x_forwarded_ultimo
        context['agente_cliente_navegador'] = obj_acesso.agente_cliente_navegador
        context['host_cliente'] = obj_acesso.host_cliente
        context['acessos'] = obj_acesso.id

        obj_lembretes = Lembrete.objects.filter(visivel = 'S').order_by('-id')
        context['nome_model_plural'] = Lembrete._meta.verbose_name_plural
        context['objects'] = obj_lembretes
        return context

    # Métodos CBVs
    # http://pythonclub.com.br/class-based-views-django.html
    def get_queryset(self,**kwargs):
        queryset = super(LembreteList, self).get_queryset()
        #queryset = queryset.filter(visivel = 'S').order_by('-id')
        #return queryset.order_by('-id')
        return self.model.filter(visivel = 'S').order_by('-id')