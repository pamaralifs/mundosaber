from django.shortcuts import render
from django.views.generic import View,TemplateView,ListView,DetailView
from .models import Acesso
from app_lembrete.models import Lembrete
from app_nivel_escolar.models import NivelEscolar
from app_serie_escolar.models import SerieEscolar
from app_material.models import Material
from django.http import FileResponse # Para fazer o download

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
        context['nome_nivel'] = NivelEscolar.objects.get(id=1)
        context['objects'] = obj_series
        context['url_listar_materiais'] = 'app_core:listar_materiais'
        return context


class EnsinoFundamental1(TemplateView):  # extend from TemplateView e NÃO TEM def query_set
    template_name = 'app_core/ensino_fundamental1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #obj_series = NivelEscolar.objects.filter(series__visivel = 'S')
        #User.objects.get(id=1).receivers.all()
        obj_series = NivelEscolar.objects.get(id=2).series.all()
        context['nome_model_plural'] = Material._meta.verbose_name_plural
        context['nome_nivel'] = NivelEscolar.objects.get(id=2)
        context['objects'] = obj_series
        context['url_listar_materiais'] = 'app_core:listar_materiais'
        return context

class EnsinoFundamental2(TemplateView):  # extend from TemplateView e NÃO TEM def query_set
    template_name = 'app_core/ensino_fundamental2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #obj_series = NivelEscolar.objects.filter(series__visivel = 'S')
        #User.objects.get(id=1).receivers.all()
        obj_series = NivelEscolar.objects.get(id=3).series.all()
        context['nome_model_plural'] = Material._meta.verbose_name_plural
        context['nome_nivel'] = NivelEscolar.objects.get(id=3)
        context['objects'] = obj_series
        context['url_listar_materiais'] = 'app_core:listar_materiais'
        return context

        #path('nivel/<int:pk>', SeriesEscolares.as_view(), name='listar_series'),
class ListarSeriesNivel(TemplateView):  # extend from TemplateView e NÃO TEM def query_set
    template_name = 'app_core/ensino_fundamental2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.nivel_id = self.kwargs['pk']
        if self.nivel_id == 1:
            self.template_name = 'app_core/educacao_infantil.html'
        elif self.nivel_id == 2:
            self.template_name = 'app_core/ensino_fundamental1.html'  
        elif self.nivel_id == 3:
            self.template_name = 'app_core/ensino_fundamental2.html'  
        obj_series = NivelEscolar.objects.get(id=self.nivel_id).series.all()
        context['nome_model_plural'] = Material._meta.verbose_name_plural
        context['nome_nivel'] = NivelEscolar.objects.get(id=self.nivel_id)
        context['objects'] = obj_series
        context['url_listar_materiais'] = 'app_core:listar_materiais'
        return context

class ListarMateriaisSerie(TemplateView):
    #model = Material
    #ordering = ['-id'] # Ou ordeno aqui
    template_name ='app_core/materiais_serie.html'
    #success_url = reverse_lazy('app_core:material_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context = super(ListarMateriaisSerie, self).get_context_data(**kwargs)
        self.serie_id = self.kwargs['pk']
        #print('serie',self.serie_id)
        if self.serie_id:
            obj_materiais = SerieEscolar.objects.get(id=self.serie_id).materiais.all().order_by('-id')
        #print('queryset',queryset)
        context['nome_model_plural'] = Material._meta.verbose_name_plural
        context['nome_serie'] = SerieEscolar.objects.get(id=self.serie_id)
        context['objects'] = obj_materiais
        context['url_download'] = 'app_core:material_download'
        print('nivel',SerieEscolar.objects.get(id=self.serie_id).nivel_escolar.id)
        if SerieEscolar.objects.get(id=self.serie_id).nivel_escolar.id == 1:
            context['url_papel_parede'] = 'assets/img/Event2.jpeg'
        elif SerieEscolar.objects.get(id=self.serie_id).nivel_escolar.id == 2:
            context['url_papel_parede'] = 'assets/img/papeldeparedef2.jpg'
        elif SerieEscolar.objects.get(id=self.serie_id).nivel_escolar.id == 3:
            context['url_papel_parede'] = 'assets/img/papeldeparede.jpg'
        return context


#DETAIL cbv específica para forçar download do arquivo, caso contrário o browser abre/visualiz o arquivo
# View DetailView para download
# https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
class MaterialDownload(DetailView):
    model = Material

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk is None:
          raise ValueError("Arquivo não encontrado!")
        obj = self.model.objects.get(id=pk)
        response = FileResponse(obj.arquivo, content_type="application/force-download")
        # https://docs.djangoproject.com/en/1.11/howto/outputting-csv/#streaming-large-csv-files
        #Informações para cabeçalho HTTP
        response['Content-Disposition'] = 'attachment; filename={}'.format(obj.arquivo.name.split('/')[-1]) #Nome para download a partir de arquivo.name do arquivo -> materiais/2020/05/11/user_1/logoescola-or.jpeg
        response['Content-Length'] = obj.arquivo.size #
        return response