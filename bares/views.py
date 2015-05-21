# -*- encoding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django import forms
from django.core.validators import validate_slug, RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from lxml import etree
from pymongo import MongoClient

class registroForm(forms.Form):
	nombre = forms.CharField (label		= 'Nombre', 
							max_length 	= 10, 
							required   	= True,)
							
	pw = forms.CharField (label		= 'Contraseña',
						required 	= True,
						widget		= forms.PasswordInput,)
							
	pw_again = forms.CharField (label		='Repita su contraseña',
								required 	= True,
								widget		= forms.PasswordInput,)
								
	email = forms.EmailField(label = 'Correo electronico')
	
	tarjeta_credito = forms.CharField( 	label = "Tarjeta de credito",
										required = True,
										max_length=16,
										validators=[
											RegexValidator(
												r'^[0-9]{16}$',
												'Se necesitan 16 dígitos',
												'Número invalido'
											),
										],
									)
									
	ano_credito = forms.CharField( 	label = "Año de expiración",
										required = True,
										max_length=4,
										validators=[
											RegexValidator(
												r'^[0-9]{4}$',
												'Se necesitan 4 dígitos',
												'Número invalido'
											),
										],
									)

	mes_credito = forms.CharField( 	label = "Mes de expiración",
										required = True,
										max_length=2,
										validators=[
											RegexValidator(
												r'[0-9]{1,2}$',
												'Se necesitan 4 dígitos',
												'Número invalido'
											),
										],
									)

	def clean (self):
		cleaned_data = super(registroForm, self).clean()
		n  = cleaned_data.get("pw")
		na = cleaned_data.get("pw_again")
		if n != na:
			raise forms.ValidationError ('Las contraseñas no coinciden')
			
class loginForm(forms.Form):
	nombre = forms.CharField (label      = 'Nombre', 
							max_length = 10, 
							required   = True,)
							
	pw = forms.CharField(	label		= 'Contraseña',
							required 	= True,
							widget		= forms.PasswordInput,)
	def clean (self):
		cleaned_data = super(loginForm, self).clean()

def index (request):
	return render(request, 'index.html')

def mi_login (request):
	# Si viene del POST del boton de submit
	if request.method == 'POST':
		form = loginForm (request.POST)
		
		# Si el formulario es valido se comprueban los credenciales
		if form.is_valid ():
			user = authenticate(username 	= form.cleaned_data['nombre'], 
								password	= form.cleaned_data['pw'])
			if user is not None:				
				if user.is_active:
					# Utilizamos la función de login de Django
					login (request, user)
					
					return redirect('bienvenida.html')
				else:
					context = {
						'mensaje':'Usuario no activo',
						'form':form,
					}
					return render(request, 'login.html', context)
			else:
				context = {
					'mensaje':'Usuario o contraseña incorrecta',
					'form':form,
				}
				return render(request, 'login.html', context)
	# Si es la primera vez que se llama (GET)
	else:
		form = loginForm()
	
		context = {
			'mensaje':'',
			'form':form,
		}
	
		return render(request, 'login.html', context)

def registrar (request):
	if request.method == 'POST':
		form = registroForm (request.POST)
		
		if form.is_valid ():
			# Creamos el usuario en la base de datos
			try:
				User.objects.create_user(username = form.cleaned_data['nombre'], 
									email = form.cleaned_data['email'],
									password = form.cleaned_data['pw']),
			except Exception as error:
				print error
				context = {
					'form':form,
					'mensaje':'Usuario existente',
				}
				return render(request, 'registrar.html', context)
		
			return redirect ('login.html')
		else:
			context =  {
				'form':form,
			}
			return render (request, 'registrar.html', context)
	else:
	
		form = registroForm()
	
		context = {
			'form':form,
		}
	
		return render(request, 'registrar.html', context)

def bienvenida (request):
	if request.user.is_authenticated():
			return render(request, 'bienvenida.html')
	else:
		return redirect('login')
		
def mi_logout (request):
	logout(request)
	return redirect('login')

def geografia(request):
	comunidad_autonoma = None 
	provincia = None
	municipio = None
	comarca = None
	
	tree = etree.parse('http://maps.googleapis.com/maps/api/geocode/xml?address=etsiit+granada&sensor=true_or_false')
	
	items = tree.xpath('/GeocodeResponse/result/address_component')
	
	for i in items:
		tipos = i.xpath('type')
		for t in tipos:
			if t.text == "administrative_area_level_1":
				nombres = i.xpath('long_name')
				if nombres:
					comunidad_autonoma = nombres[0]
			elif t.text == "administrative_area_level_2":
				nombres = i.xpath('long_name')
				if nombres:
					provincia = nombres[0]
			elif t.text == "administrative_area_level_3":
				nombres = i.xpath('long_name')
				if nombres:
					municipio = nombres[0]
			elif t.text == "administrative_area_level_4":
				nombres = i.xpath('long_name')
				if nombres:
					comarca = nombres[0]

	context = {
		'ca':comunidad_autonoma.text,
		'provincia':provincia.text,
		'municipio':municipio.text,
		'comarca':comarca.text,
	}

	return render(request, 'geografia.html', context)

def imagenes_rss(request):
	tree = etree.parse('http://ep00.epimg.net/rss/tecnologia/portada.xml')
	
	imagenes = tree.xpath('//enclosure/@url')
	
	# Buscamos la imagen de cabecera y la añadimos a la lista de imángees
	# en formato de texto
	imagen_extra = tree.xpath('//image/url')
	imagenes.append(imagen_extra[0].text)
	
	context = {
		'imagenes':imagenes,
	}
	
	return render(request, 'imagenes_rss.html', context)

def crawler_rss(request):
	mongo_cliente = MongoClient()
	db = mongo_cliente.db
	coleccion = db.coleccion

	if request.method == 'POST':
		noticias = coleccion.find({"categorias":request.POST.get("categoria","")})
		
		context = {
			'noticias':noticias,
		}
		
		return render(request, 'crawler_rss.html', context)
	else:
		mongo_cliente.db.coleccion.remove()
		
		tree = etree.parse('http://ep00.epimg.net/rss/tecnologia/portada.xml')
		
		items = tree.xpath('//item')
		
		for i in items:
			titulo_temp = i.xpath('title')
			if titulo_temp:
				titulo = titulo_temp[0].text.encode('utf-8')
			
			link_temp = i.xpath('link')
			if link_temp:
				link = link_temp[0].text.encode('utf-8')
			
			text_temp = i.xpath('description')
			if text_temp:
				text = text_temp[0].text.encode('utf-8')
			
			categorias = []
			categorias_temp = i.xpath('category')
			
			for c in categorias_temp:
				categorias.append(c.text.encode('utf-8'))
				
			noticia = {
				'titulo':titulo,
				'link':link,
				'categorias':categorias,
				'text':text,
			}
			
			coleccion.insert_one(noticia).inserted_id
		
		print(coleccion.count())
	
	return render(request, 'crawler_rss.html')

def crawler_rss_actualizar(request):
	mongo_cliente = MongoClient()
	db = mongo_cliente.db
	coleccion = db.coleccion
	
	mongo_cliente.db.coleccion.remove()
	
	numero_items = 0
	
	tree = etree.parse('http://ep00.epimg.net/rss/tecnologia/portada.xml')
	
	items = tree.xpath('//item')
	
	for i in items:
		numero_items += 1
		titulo_temp = i.xpath('title')
		if titulo_temp:
			titulo = titulo_temp[0].text.encode('utf-8')
		
		link_temp = i.xpath('link')
		if link_temp:
			link = link_temp[0].text.encode('utf-8')
		
		text_temp = i.xpath('description')
		if text_temp:
			text = text_temp[0].text.encode('utf-8')
			
		categorias = []
		categorias_temp = i.xpath('category')
		
		for c in categorias_temp:
			categorias.append(c.text.encode('utf-8'))
			
		noticia = {
			'titulo':titulo,
			'link':link,
			'categorias':categorias,
			'text':text,
		}
		
		coleccion.insert_one(noticia).inserted_id
		
	return JsonResponse({'num_noticias':numero_items})
