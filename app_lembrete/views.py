from django.shortcuts import render
from django.urls import reverse_lazy #
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView #
from django.contrib.auth.mixins import LoginRequiredMixin #
from django.contrib.messages.views import SuccessMessageMixin #
#from django.views.generic.edit import FormView #
from .models import Lembrete #
from .forms import LembreteForm1Filtro
from datetime import datetime #
#import os 
from django.core.paginator import Paginator # Para obter o total de páginas da paginação da ListView
# Create your views here.

#VISTAS CRUDs
#CREATE
class LembreteCreate(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Lembrete
    fields = ['titulo','conteudo','visivel'] #removi os campos 'usuario' e 'nivel_escolar' e pego eles no def form_valid
    success_url = reverse_lazy('app_lembrete:lembrete_create')
    success_message = ''

    def get_context_data(self, **kwargs):
        context = super(LembreteCreate, self).get_context_data(**kwargs)
        context['nome_model'] = self.model._meta.verbose_name
        #context['nome_model_plural'] = self.model._meta.verbose_name_plural
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user  #Necessário para criar o path do armazenamento
        form.instance.data_hora_cadastro = datetime.now() #Necessário para criar o path do armazenamento
        if self.request.POST['visivel'] == 'S':
            self.success_message = self.model._meta.verbose_name + ' <strong>SALVO</strong> e <strong>PUBLICADO</strong> com sucesso! (Visível = Sim)'
        else:
            self.success_message = self.model._meta.verbose_name + ' <strong>SALVO</strong> com sucesso, <strong>PORÉM NÃO PUBLICADO</strong>! (Visível = Não)'
        return super(LembreteCreate, self).form_valid(form)

#READ
class LembreteList(LoginRequiredMixin, ListView):
    model = Lembrete
    ordering = ['-id'] # Ou ordeno aqui
    form_class = LembreteForm1Filtro
    paginate_by = 3
    # queryset = Lembrete.objects.all().order_by('-id') # Ou ordeno aqui

    # Métodos CBVs
    # http://pythonclub.com.br/class-based-views-django.html

    def get_queryset(self,**kwargs):
        queryset = super(LembreteList, self).get_queryset()
        self.search = self.request.GET.get('search','')  # Texto do título/nome/descrição
        self.type = self.request.GET.get('type','')      # Modo de busca (listar todos, contenha, inicie com, termine com)
        self.page = self.request.GET.get('page','')
        # Cria variáveis de sessão para montar o success_url das views Update, Delete (de alterar e excluir) porque não tem com repassar via atributo de instância self
        self.request.session['search'] = self.search
        self.request.session['type'] = self.type
        self.request.session['page'] = self.page
        # Como a View foi criada com ordem decrescente de id
        # Neste def query_set se eu não retornar também os resultados ordenados decrescente, dá erro
        if self.search:
            if self.type == '0': # listar todos
                queryset = self.model.objects.all().order_by('-id')
            elif self.type == '1':
                queryset = queryset.filter(titulo__icontains = self.search).order_by('-id') # contenha
            elif self.type == '2':
                queryset = queryset.filter(titulo__startswith = self.search).order_by('-id') # inicie com
            elif self.type == '3':
                queryset = queryset.filter(titulo__endswith = self.search).order_by('-id') # termine com
        else:
            queryset = self.model.objects.all().order_by('-id')
        # Cria variável de sessão total_páginas para usar na DeletView
        paginator = Paginator(queryset, self.paginate_by)
        self.request.session['total_de_paginas'] = paginator.num_pages

        # Cria a variável de sessão total total_registros_da_pagina
        if paginator.page_range:
            if self.page: # se página atual possui valor
                self.request.session['total_registros_da_pagina'] = len(paginator.page(self.page))
            else: # se não é porque está é a página 1 e a variável GET page veio vazia após filtragem e não navegação
                self.request.session['total_registros_da_pagina'] = len(paginator.page(min(paginator.page_range)))         
        #else:
        #    print('não tem páginas')
        self.total_registros = queryset.count() #total geral de registros filtrados      
        return queryset.order_by('-id')
            
        # return self.model.filter(user=request.user)  self.model suporta filter???

    def get_context_data(self, **kwargs):
        context = super(LembreteList, self).get_context_data(**kwargs)
        # Pega o contexto do formulário e cria outras variáveis de contexto mais embaixo
        context['form'] = LembreteForm1Filtro
        # Outras variáveis de contexto
        context['search'] = self.search
        context['type'] = self.type
        context['page'] = self.page
        context['total_registros'] = self.total_registros # Total de registros filtrados
        context['nome_model'] = self.model._meta.verbose_name
        context['nome_model_plural'] = self.model._meta.verbose_name_plural
        context['url_novo'] = 'app_' + self.model._meta.verbose_name.lower() + ':' + self.model._meta.verbose_name.lower() + '_create' #no template a tag url teria 'app_lembrete:lembrete_create'
        context['url_alterar'] = 'app_' + self.model._meta.verbose_name.lower() + ':' + self.model._meta.verbose_name.lower() + '_update'
        context['url_excluir'] = 'app_' + self.model._meta.verbose_name.lower() + ':' + self.model._meta.verbose_name.lower() + '_delete'
        context['url_detalhe'] = 'app_' + self.model._meta.verbose_name.lower() + ':' + self.model._meta.verbose_name.lower() + '_detail'
        return context
    

#UPDATE 
class LembreteUpdate(LoginRequiredMixin,UpdateView):
    model = Lembrete
    fields = ['titulo','conteudo','visivel'] # removi os campos 'usuario' e 'nivel_escolar' e pego eles no def form_valid
    # Inicialmente coloquei essa success_url, mas no método form_valid eu retorno para página da paginação atual e funciona, mas na deleção não (na deleção tive que usar o dispatch)
    success_url = reverse_lazy('app_lembrete:lembrete_read') # se colocar lembrete_update para ver mensagens dá erro, por isso tirei o SuccessMessageMixin
    #success_message = ''

    def get_context_data(self, **kwargs):
        context = super(LembreteUpdate, self).get_context_data(**kwargs)
        context['nome_model'] = self.model._meta.verbose_name
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # Necessário para criar o path do armazenamento
        form.instance.data_hora_alteracao = datetime.now() 
        # Monta a success_url com as variáveis de sessão
        self.success_url = reverse_lazy('app_lembrete:lembrete_read') + '?search=' + self.request.session['search'] + '&type=' + self.request.session['type'] + '&page=' + self.request.session['page']
        # Deleta as variáveis de sessão <- NÃO DELETAR PORQUE PRECISA PARA OPERAÇÃO DE DELETAR E DETALHES
        #del self.request.session['search']
        #del self.request.session['type']
        #del self.request.session['page']
        return super(LembreteUpdate, self).form_valid(form)

#DELETE
class LembreteDelete(LoginRequiredMixin, DeleteView):
    model = Lembrete
    #success_url = reverse_lazy('app_lembrete:lembrete_read')

    def dispatch(self, request, *args, **kwargs):
        # ESTE MÉTODO É O RECOMENDADO PARA INICIALIZAR UMA VIEW
        # https://stackoverflow.com/questions/46599145/django-class-view-init
        # E NELE FAÇO A MONTAGEM DA success_url PORQUE UMA DETERMINADA PÁGINA PODE DEIXAR DE EXISTIR NA DELEÇÃO E NÃO SER O PARÂMETRO ATUAL GET '&page='
        # POR, NO CASO DE DELEÇÃO DE REGISTRO, NÃO FUNCIONA MONTANDO-A NOS MÉTODOS GET_CONTEXT_DATA E FORM_VALID
        if self.request.session['total_registros_da_pagina']:
            tota_registros_da_pagina = int(self.request.session['total_registros_da_pagina'])
            if tota_registros_da_pagina == 1:
                if self.request.session['page']: # se página atual possui valor, ou seja, o parâmetro GET '&page=' não está vazio
                    pagina_atual = int(self.request.session['page'])
                else: # se não é porque está é a página 1 e a variável GET page veio vazia após a imediata filtragem (sem navegar para outra página) e apenas ratifico o valor para 1
                    pagina_atual = 1
            if tota_registros_da_pagina == 1 and pagina_atual != 1: # se o total de registros da página for 1 e a página for diferente da primeira,
                # subtraio o valor do parâmetro GET '&page=' retrocedendo a filtragem para a página anterior ao retornar para a página de listagem após a deleção do registro
                self.success_url = reverse_lazy('app_lembrete:lembrete_read') + '?search=' + self.request.session['search'] + '&type=' + self.request.session['type'] + '&page=' + str(pagina_atual - 1)
            else:
                # caso contrário, mantenho o parâmetro GET '&page='
                self.success_url = reverse_lazy('app_lembrete:lembrete_read') + '?search=' + self.request.session['search'] + '&type=' + self.request.session['type'] + '&page=' + self.request.session['page']
        return super(LembreteDelete, self).dispatch(request, *args, **kwargs)

    # TIVE que usar este método (funciona como se fosse um __init__, pois em views não se deve sobrescrever o __init__)
    # Usei porque a cbv Delete view não estava aceitando a montagem da success_url com parâmetros GET de filtragem nos métodos get_context_data nem no form_valid
    def get_context_data(self, **kwargs):
        context = super(LembreteDelete, self).get_context_data(**kwargs)
        context['nome_model'] = self.model._meta.verbose_name
        return context


#DETAIL
class LembreteDetail(LoginRequiredMixin, DetailView):
    model = Lembrete

    def get_context_data(self, **kwargs):
        context = super(LembreteDetail, self).get_context_data(**kwargs)
        # Outras variáveis de contexto
        context['nome_model'] = self.model._meta.verbose_name
        context['url_alterar'] = 'app_' + self.model._meta.verbose_name.lower() + ':' + self.model._meta.verbose_name.lower() + '_update'
        context['url_excluir'] = 'app_' + self.model._meta.verbose_name.lower() + ':' + self.model._meta.verbose_name.lower() + '_delete'
        return context

#DETAIL cbv específica para forçar download do arquivo, caso contrário o browser abre/visualiz o arquivo
# View DetailView para download
# https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
class LembreteDownload(LoginRequiredMixin, ListView):
    model = Lembrete

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
