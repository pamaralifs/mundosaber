"""mundodosaber URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings #
from django.conf.urls.static import static # para incluir diretórios MEDIA

urlpatterns = [
    path('',include('app_core.urls',namespace='app_core')),
    path('material/',include('app_material.urls','app_material')),
    path('lembrete/',include('app_lembrete.urls','app_lembrete')),
    path('restrito/admin/', admin.site.urls),
    #path('admin/restrito', admin.site.urls),
    #path('admin/', admin.site.urls),
]

# Apenas para servir arquivo de media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('usuario/', include('django.contrib.auth.urls')),
]
