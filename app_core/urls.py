from django.urls import path #
from .views import * #

app_name = 'app_core'

urlpatterns = [
    path('', Home.as_view(),name='home'),
    path('ensino/<int:pk>', ListarSeriesNivel.as_view(), name='listar_series_nivel'),
    path('materiais/<int:pk>', ListarMateriaisSerie.as_view(), name='listar_materiais'),
    path('download/<int:pk>', MaterialDownload.as_view(), name='material_download'),
]