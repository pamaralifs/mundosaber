from django.urls import path #
from .views import * #

app_name = 'app_core'

urlpatterns = [
    path('', Home.as_view(),name='home'),
    path('einfantil/', EducacaoInfantil.as_view(), name='educacao_infantil'),
    path('efuntamental1/', EnsinoFundamental1.as_view(), name='ensino_fundamental_I'),
    path('efuntamental2/', EnsinoFundamental2.as_view(), name='ensino_fundamental_II'),
]