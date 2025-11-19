"""Configuración de las rutas URL para la aplicación AppHidroZen."""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('api/humedad/', views.obtener_humedad_actual, name='api_humedad'),
    path('registrar_ip/', views.registrar_ip, name='registrar_ip'),
    path('obtener_ip/', views.obtener_ip, name='obtener_ip'),
    path("", views.home, name="home"),  # Ruta para la página de inicio
    path("login/", views.login_view, name="login"),  # Ruta para la página de login
    path("registro/", views.registro_view, name="registro"),
    path("programacion_automatica/", views.programacion_automatica_view, name="programacion_automatica"),
    path("inicio/", views.inicio_view, name="inicio"),
    path("riego_manual/", views.riego_manual_view, name="riego_manual"),
    path("api/riego/manual/activar/", views.activar_riego_manual, name="activar_riego_manual"),
    path("api/riego/manual/desactivar/", views.desactivar_riego_manual, name="desactivar_riego_manual"),
    path("api/riego/manual/activar_por_tiempo/", views.activar_riego_por_tiempo, name="activar_riego_por_tiempo"),
    path("esp32/registrar_ip/", views.recibir_ip_esp32, name="recibir_ip_esp32"),
]

urlpatterns+=static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)




