"""HidroComp_TCC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url

from . import views

app_name = 'dados'

urlpatterns = [
    url(r'index/', views.results_index, name='index'),
    url(r'sampling_feature/', views.sampling_feature, name='samplingfeature'),
    url(r'methods/', views.methods, name='methods'),
    url(r'actions/', views.actions, name='actions'),
    url(r'feature/', views.feature, name='feature'),
    url(r'results/', views.results, name='results'),
    url(r'units/', views.units, name='units'),
    url(r'processing_level', views.processing_level, name='processinglevel'),
    url(r'variables/', views.variables, name='variables'),
    url(r'organizations/', views.organizations, name='organizations'),
    url(r'time_serie_result/', views.time_serie_result, name='time_serie_result'),
    url(r'time_serie/', views.time_series, name='time_serie')
]