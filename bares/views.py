from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.core.validators import validate_slug, RegexValidator

class registrationForm(forms.Form):
	name = forms.CharField (label      = 'Nombre', 
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
			raise forms.ValidationError ('los nombres no coinciden')

def index (request):
	return render(request, 'index.html')

def registrar (request):
	if request.method == 'POST':
		form = registrationForm (request.POST)
		
		if form.is_valid ():
			context =  {
				'fulanito':form.cleaned_data['name'],
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
	
		form = registrationForm()
	
		context = {
			'fulanito':fulanito,
			'form':form,
		}
	
		return render(request, 'registrar.html', context)

def registro (request, fulanito):
	context = {
		'fulanito':fulanito,
	}
	return render(request, 'index.html', context)
