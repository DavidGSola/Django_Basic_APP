from django.conf.urls import patterns, url

from bares import views

urlpatterns = patterns ('',
	url(r'^$', views.index, name='index'),
	url(r'^registrar', views.registrar, name='registrar'),
	url(r'^registro_de_(?P<fulanito>\w+)', views.registro, name='registro'),
)
