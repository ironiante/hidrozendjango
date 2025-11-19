"""Definición de modelos de datos para la aplicación AppHidroZen.

Incluye modelos para las plantas gestionadas, sus datos de riego y configuraciones personalizadas.
"""

from django.db import models


class Planta(models.Model):
    """Representa una planta registrada en el sistema de riego.

    Atributos:
        nombre (str): Nombre asignado a la planta.
        especie (str): Especie o tipo de la planta.
        necesita_riego (bool): Indica si la planta requiere riego actualmente.
        riego_automatico (bool): Define si la planta está en modo de riego automático.
    """

    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=100)
    necesita_riego = models.BooleanField(default=False)
    riego_automatico = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.nombre} ({self.especie})"


class DatosRiego(models.Model):
    """Registros de datos de riego de una planta.

    Atributos:
        planta (Planta): Referencia a la planta asociada.
        humedad_suelo (decimal): Porcentaje de humedad del suelo.
        temperatura_ambiente (decimal): Temperatura ambiente en °C.
        fecha_riego (datetime): Fecha y hora del registro.
        cantidad_agua (int): Cantidad de agua en mililitros.
    """

    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    humedad_suelo = models.DecimalField(max_digits=5, decimal_places=2)
    temperatura_ambiente = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_riego = models.DateTimeField(auto_now_add=True)
    cantidad_agua = models.IntegerField(help_text="Cantidad de agua en mililitros")

    def __str__(self):
        return f"Riego - {self.planta.nombre} - {self.fecha_riego.strftime('%Y-%m-%d %H:%M')}"


class Configuracion(models.Model):
    """Configuración de riego para una planta.

    Atributos:
        planta (Planta): Referencia única a la planta.
        nivel_minimo_humedad (decimal): Humedad mínima permitida antes de regar.
        frecuencia_riego (str): Frecuencia con la que se realiza el riego.
        notificaciones (bool): Indica si se envían notificaciones.
    """

    planta = models.OneToOneField(Planta, on_delete=models.CASCADE)
    nivel_minimo_humedad = models.DecimalField(max_digits=5, decimal_places=2)
    frecuencia_riego = models.CharField(max_length=50)
    notificaciones = models.BooleanField(default=True)

    def __str__(self):
        return f"Config - {self.planta.nombre}"

