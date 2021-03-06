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
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.conf.urls import url, include

from ajax_select import views as ajax_select_views
from core import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^lookups/(?P<channel>[-\w]+)$', ajax_select_views.ajax_lookup,name='ajax_lookup'),
    url(r'^$', views.index, name='index'),
    url('reduction/', include('reduction.urls'), name='reduction'),
    url('dados/', include('core.urls'), name='dados'),
    url(r'^entrar/$', LoginView.as_view(template_name='sign_in.html'), name='login'),
    url(r'^sair/$',  LogoutView.as_view(template_name='index.html'), name='logout'),

]
