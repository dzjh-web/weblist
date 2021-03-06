"""weblist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.views.static import serve
from django.urls import path
from django.conf.urls import url, include

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditorView

from weblist import settings
from DBModel import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^game$', views.game),
    url(r'^web$', views.webkit),
    url(r'^resume$', views.resume),
    url(r'^release$', views.release),
    url(r'^media/(?P<path>.*)', serve, {"document_root":settings.MEDIA_ROOT}),
    url(r'^ckeditor/upload/', csrf_exempt(views.checkToken(ckeditorView.upload)), name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(views.checkToken(ckeditorView.browse)), name='ckeditor_browse'),
]
