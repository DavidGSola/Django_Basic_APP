from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index (request):
	return HttpResponse ("Hola desde bares/")

def registro (request, fulanito):
	context = {
		'fulanito':fulanito,
	}
	return render(request, 'index.html', context)
