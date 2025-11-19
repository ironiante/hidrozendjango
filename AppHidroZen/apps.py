"""Configuración de la aplicación AppHidroZen para el proyecto Django."""

from django.apps import AppConfig


class ApphidrozenConfig(AppConfig):
    """Configuración de la aplicación AppHidroZen.

    Esta clase define los ajustes específicos para la app dentro del proyecto Django.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "AppHidroZen"

