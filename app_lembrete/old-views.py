from django.shortcuts import render
from django.urls import reverse_lazy #
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView #
from django.contrib.auth.mixins import LoginRequiredMixin #
from django.contrib.messages.views import SuccessMessageMixin #
#from django.views.generic.edit import FormView #
from .models import Lembrete
#from .forms import FormMaterial #
from datetime import datetime #
#import os #

# Create your views here.

#VISTAS CRUDs
#CREATE
class LembreteCreate(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Lembrete
    fields = ['titulo','conteudo','visivel',] #removi o campo usuario e pego ele no def form_valid
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
class LembreteList(ListView):
    model = Lembrete
    ordering = ['-id']

#UPDATE 
class LembreteUpdate(LoginRequiredMixin, UpdateView):
    model = Lembrete
    success_url = reverse_lazy('app_lembrete:lembrete_read')

#DELETE
class LembreteDelete(LoginRequiredMixin, DeleteView):
    model = Lembrete
    success_url = reverse_lazy('app_lembrete:lembrete_read')

#DETAIL
class LembreteDetail(DetailView):
    model = Lembrete
