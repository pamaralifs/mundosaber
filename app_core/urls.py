from django.urls import path #
from .views import * #

app_name = 'app_core'

urlpatterns = [
    path('', Home.as_view()),
    #path('create/', MaterialCreate.as_view(), name='material_create'),
    #path('read/', MaterialList.as_view(), name='material_read'),
    #path('update/<int:pk>', MaterialUpdate.as_view(), name='material_update'),
    #path('delete/<int:pk>', MaterialDelete.as_view(), name='material_delete'),
    #path('detail/<int:pk>', MaterialDetail.as_view(), name='material_detail'),
]