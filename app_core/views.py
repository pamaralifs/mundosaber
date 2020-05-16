from django.shortcuts import render
from django.views.generic import View,TemplateView,ListView
from .models import Acesso
from app_lembrete.models import Lembrete
from app_nivel_escolar.models import NivelEscolar
from app_serie_escolar.models import SerieEscolar
from app_material.models import Material

# Create your views here.

#HOME
class Home(TemplateView):  # extend from TemplateView e NÃO TEM def query_set
    template_name = 'app_core/index.html'

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

class EducacaoInfantil(TemplateView):  # extend from TemplateView e NÃO TEM def query_set
    template_name = 'app_core/educacao_infantil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #obj_series = NivelEscolar.objects.filter(series__visivel = 'S')
        #User.objects.get(id=1).receivers.all()
        obj_series = NivelEscolar.objects.get(id=1).series.all()
        context['nome_model_plural'] = Material._meta.verbose_name_plural
        context['objects'] = obj_series
        return context


class EnsinoFundamental1(TemplateView):  # extend from TemplateView e NÃO TEM def query_set
    template_name = 'app_core/ensino_fundamental1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['now'] = datetime.now()
        return context

class EnsinoFundamental2(TemplateView):  # extend from TemplateView e NÃO TEM def query_set
    template_name = 'app_core/ensino_fundamental2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['now'] = datetime.now()
        return context