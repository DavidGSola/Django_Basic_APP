from django.contrib import admin
from bares.models import Bares, Tapas

class linea_tapas (admin.StackedInline):
	model = Tapas
	extra = 2

class BaresAdmin(admin.ModelAdmin):
	fieldsets = [
        (None,               {'fields': ['nombre']}),
        (None,               {'fields': ['direccion']}),
        ('Fecha visita',     {'fields': ['fecha_visita'], 'classes': ['collapse']}),
    ]
	inlines = [linea_tapas]
	list_display = ('nombre', 'direccion', 'fecha_visita')
	list_filter = ['fecha_visita']
	search_fields = ['nombre']

admin.site.register(Bares, BaresAdmin)
