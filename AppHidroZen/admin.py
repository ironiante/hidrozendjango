"""Configuración del panel de administración para la aplicación AppHidroZen."""

from django.contrib import admin
from .models import Planta, DatosRiego, Configuracion

# Personalización básica del sitio admin
admin.site.site_header = "HidroZen — Administración"
admin.site.site_title = "HidroZen Admin"
admin.site.index_title = "Panel de control"

@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "especie", "necesita_riego", "riego_automatico")
    search_fields = ("nombre", "especie")
    list_filter = ("riego_automatico", "necesita_riego")
    ordering = ("id",)

@admin.register(DatosRiego)
class DatosRiegoAdmin(admin.ModelAdmin):
    list_display = ("id", "planta", "humedad_suelo", "temperatura_ambiente", "fecha_riego", "cantidad_agua")
    search_fields = ("planta__nombre",)
    list_filter = ("fecha_riego",)
    date_hierarchy = "fecha_riego"
    ordering = ("-fecha_riego",)

@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ("id", "planta", "nivel_minimo_humedad", "frecuencia_riego", "notificaciones")
    search_fields = ("planta__nombre", "frecuencia_riego")
    list_filter = ("notificaciones",)
    ordering = ("id",)
