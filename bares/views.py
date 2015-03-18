# -*- encoding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.core.validators import validate_slug, RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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
	return render(request, 'bienvenida.html')

def mi_logout (request):
	logout(request)
	return redirect('login')
