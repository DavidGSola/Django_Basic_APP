from django.conf.urls import patterns, url

from bares import views

urlpatterns = patterns ('',
	url(r'^$', views.index, name='index'),
	url(r'^login', views.login, name='login'),
	url(r'^registrar', views.registrar, name='registrar'),
)
