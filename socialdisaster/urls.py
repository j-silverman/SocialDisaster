"""socialdisaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dammap/', TemplateView.as_view(template_name="dammap.html"),name='dammap'),
    url(r'^medmap/', TemplateView.as_view(template_name="medmap.html"),name='medmap'),
    url(r'^sheltmap/', TemplateView.as_view(template_name="sheltmap.html"),name='sheltmap'),
    url(r'^evacmap/', TemplateView.as_view(template_name="evactmap.html"),name='evacmap'),
    url(r'^customtags/$', views.customtags, name= 'customtags'),
    url(r'^admin/', admin.site.urls),
]
