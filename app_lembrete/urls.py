from django.urls import path #
from .views import * #

app_name = 'app_lembrete'

urlpatterns = [
    path('create/', LembreteCreate.as_view(), name='lembrete_create'),
    path('read/', LembreteList.as_view(), name='lembrete_read'),
    path('update/<int:pk>', LembreteUpdate.as_view(), name='lembrete_update'),
    path('delete/<int:pk>', LembreteDelete.as_view(), name='lembrete_delete'),
    path('detail/<int:pk>', LembreteDetail.as_view(), name='lembrete_detail'),
]