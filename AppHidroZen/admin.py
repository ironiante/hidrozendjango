"""Configuración del panel de administración para la aplicación AppHidroZen."""

from django.contrib import admin
from .models import Planta, DatosRiego, Configuracion

admin.site.register(Planta)
admin.site.register(DatosRiego)
admin.site.register(Configuracion)



