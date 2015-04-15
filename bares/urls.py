from django.conf.urls import patterns, url

from bares import views

urlpatterns = patterns ('',
	url(r'^$', views.index, name='index'),
	url(r'^login', views.mi_login, name='login'),
	url(r'^registrar', views.registrar, name='registrar'),
	url(r'^bienvenida', views.bienvenida, name='bienvenida'),
	url(r'^logout', views.mi_logout, name='logout'),
	url(r'^geografia', views.geografia, name='geografia'),
	url(r'^imagenes_rss', views.imagenes_rss, name='imagenes_rss'),
	url(r'^crawler_rss_actualizar', views.crawler_rss_actualizar, name='crawler_rss_actualizar'),
	url(r'^crawler_rss', views.crawler_rss, name='crawler_rss'),
)
