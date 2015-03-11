from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.core.validators import validate_slug, RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class registroForm(forms.Form):
	nombre = forms.CharField (label      = 'Nombre', 
							max_length = 10, 
							required   = True,)
							
	pw = forms.CharField(	label		= 'Contrasena',
							required 	= True,
							widget		= forms.PasswordInput,)
							
	pw_again = forms.CharField (label		='Repita su contrasena',
								required 	= True,
								widget		= forms.PasswordInput,)
								
	email = forms.EmailField(label = 'Correo electronico')

	def clean (self):
		cleaned_data = super(registrationForm, self).clean()
		n  = cleaned_data.get("pw")
		na = cleaned_data.get("pw_again")
		if n != na:
			raise forms.ValidationError ('los contrasnas no coinciden')
			
class loginForm(forms.Form):
	nombre = forms.CharField (label      = 'Nombre', 
							max_length = 10, 
							required   = True,)
							
	pw = forms.CharField(	label		= 'Contrasena',
							required 	= True,
							widget		= forms.PasswordInput,)
	def clean (self):
		cleaned_data = super(loginForm, self).clean()

def index (request):
	return render(request, 'index.html')

def login (request):
	if request.method == 'POST':
		form = loginForm (request.POST)
		
		if form.is_valid ():
			user = authenticate(username 	= form.cleaned_data['nombre'], 
								password	= form.cleaned_data['pw'])
			if user is not None:
				if user.is_active:
					print("User is valid, active and authenticated")
				else:
					print("The password is valid, but the account has been disabled!")
			else:
				# the authentication system was unable to verify the username and password
				print("The username and password were incorrect.")
	else:
		fulanito = 'default'
	
		form = loginForm()
	
		context = {
			'fulanito':fulanito,
			'form':form,
		}
	
		return render(request, 'login.html', context)

def registrar (request):
	if request.method == 'POST':
		form = registroForm (request.POST)
		
		if form.is_valid ():
			User.objects.create(username 	= form.cleaned_data['nombre'], 
								email		= form.cleaned_data['email'],
								password	= form.cleaned_data['pw']),
			context =  {
				'fulanito':form.cleaned_data['nombre'],
				'form':form,
			}

			return render (request, 'index.html', context)
		else:
			context =  {
				'fulanito': 'error',
				'form':form,
			}
			return render (request, 'index.html', context)
	else:
		fulanito = 'default'
	
		form = registroForm()
	
		context = {
			'fulanito':fulanito,
			'form':form,
		}
	
		return render(request, 'registrar.html', context)
