from django.views.decorators.csrf import csrf_exempt

import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import DatosRiego
import json
import logging

logger = logging.getLogger(__name__) 

# IP del ESP32
#ESP32_IP = "http://192.168.20.6"

def inicio_view(request):
    ip_esp32 = obtener_ip_esp32()
    print(f"🧪 IP que se pasa al template: {ip_esp32}")
    return render(request, "AppHidroZen/inicio.html", {"esp32_ip": ip_esp32})

# Función para registrar IP enviada por la ESP32
@csrf_exempt
def registrar_ip(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ip = data.get("ip")
        print(f"📡 IP recibida desde ESP32: {ip}")
        return JsonResponse({"status": "ok", "ip": ip})
    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)


# --- Función para obtener IP del ESP32 desde archivo ---
def obtener_ip_esp32():
    try:
        with open("esp32_ip.txt", "r") as f:
            ip = f.read().strip()
            return f"http://{ip}"
    except FileNotFoundError:
        return "http://192.168.20.6"  # Valor por defecto
    

# --- Vista para responder la IP al frontend ---
def obtener_ip(request):
    ip = obtener_ip_esp32()
    return JsonResponse({"ip": ip})





# ESP32_IP = obtener_ip_esp32()


# --- API en Django para entregar el último valor ---

def obtener_humedad_actual(request):
    ultimo = DatosRiego.objects.last()
    valor = float(ultimo.humedad_suelo) if ultimo else 0.0
    return JsonResponse({'humedad': valor})

# --- Vistas para renderizar plantillas HTML ---

def home(request):
    """Página de inicio."""
    ip_esp32 = obtener_ip_esp32()
    return render(request, "AppHidroZen/home.html", {"esp32_ip": ip_esp32})
# ✅ Ruta corregida

def login_view(request):
    """Página de inicio de sesión."""
    return render(request, "AppHidroZen/login.html")  # ✅ Asume que login.html está en la misma carpeta

def registro_view(request):
    """Página de registro de usuarios."""
    return render(request, "AppHidroZen/registro.html")

def programacion_automatica_view(request):
    """Configuración de riego automático."""
    return render(request, "AppHidroZen/programacion_automatica.html")

def inicio_view(request):
    #"""Inicio principal tras login."""
    ip_esp32 = obtener_ip_esp32()  # Lee la IP desde el archivo
    return render(request, "AppHidroZen/inicio.html", {"esp32_ip": ip_esp32})
# return render(request, "AppHidroZen/inicio.html")

def riego_manual_view(request):
    """Interfaz de control manual del riego."""
    return render(request, "AppHidroZen/riego_manual.html")

# --- API para controlar el ESP32 ---

@csrf_exempt
def activar_riego_manual(request):
    """
    Vista API para activar el riego manual en el ESP32.
    Espera una petición POST.
    """
    if request.method == "POST":
        try:
            # Construye la URL para la petición al ESP32
            # CORREGIDO: Cambiado de /manual/start a /manual/activar
            esp32_ip = obtener_ip_esp32()
            url = f"{esp32_ip}/manual/activar"
            logger.info(f"Intentando conectar a: {url}")
            response = requests.get(url, timeout=5)# El ESP32 espera GET
            logger.info(f"Respuesta del ESP32 (código de estado): {response.status_code}")
            if response.status_code == 200:
                return JsonResponse({"success": True})
            else:
                # Si el ESP32 devuelve un error, se lo indica al cliente
                logger.error(f"Error en ESP32. Código de estado: {response.status_code}, Contenido: {response.text}")
                return JsonResponse({"success": False, "error":  f"Error en ESP32: {response.text}"}, status=response.status_code)
        except requests.RequestException as e:
            # Captura errores de conexión o de la petición
            logger.error(f"Error de conexión al ESP32: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
        except Exception as e:
            # Captura cualquier otro error inesperado
            logger.error(f"¡Error inesperado en activar_riego_manual!: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    logger.warning(f"Intento de acceder a activar_riego_manual con método no permitido: {request.method}")
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)


@csrf_exempt
def desactivar_riego_manual(request):
    """
    Vista API para desactivar el riego manual en el ESP32.
    Espera una petición POST.
    """
    if request.method == "POST":
        try:
            # Construye la URL para la petición al ESP32
            # CORREGIDO: Cambiado de /manual/start a /manual/desactivar
            esp32_ip = obtener_ip_esp32()
            url = f"{esp32_ip}/manual/desactivar"
            logger.info(f"Intentando conectar a: {url}")
            response = requests.get(url, timeout=5) # El ESP32 espera GET
            logger.info(f"Respuesta del ESP32 (código de estado): {response.status_code}")
            if response.status_code == 200:
                return JsonResponse({"success": True})
            else:
                # Si el ESP32 devuelve un error, se lo indica al cliente
                logger.error(f"Error en ESP32. Código de estado: {response.status_code}, Contenido: {response.text}")
                return JsonResponse({"success": False, "error": f"Error en ESP32: {response.text}"}, status=response.status_code)
        except requests.RequestException as e:
            # Captura errores de conexión o de la petición
            logger.error(f"Error de conexión al ESP32: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
        except Exception as e:
            # Captura cualquier otro error inesperado
            logger.error(f"¡Error inesperado en desactivar_riego_manual!: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    logger.warning(f"Intento de acceder a desactivar_riego_manual con método no permitido: {request.method}")
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

@csrf_exempt
def activar_riego_por_tiempo(request):
    """
    Vista API para activar el riego por un tiempo específico en el ESP32.
    Espera una petición POST con un JSON que contenga la duración.
    """
    if request.method == "POST":
        try:
            # Carga los datos JSON del cuerpo de la petición
            data = json.loads(request.body)
            # Obtiene la duración de los datos, por defecto 0 si no se encuentra
            duration = int(data.get("duration", 0))

            # Valida que la duración sea un valor positivo
            if duration <= 0:
                return JsonResponse({"success": False, "error": "Duración inválida"}, status=400)

            # Construye la URL para la petición al ESP32 con la duración
            # La ruta /manual/activar_duracion es la correcta en el ESP32
            esp32_ip = obtener_ip_esp32()
            url = f"{esp32_ip}/manual/activar_duracion?duracion={duration}"
            logger.info(f"Intentando conectar a: {url}")
            response = requests.get(url, timeout=5) # El ESP32 espera GET
            logger.info(f"Respuesta del ESP32 (código de estado): {response.status_code}")
            if response.status_code == 200:
                return JsonResponse({"success": True})
            else:
                # Si el ESP32 devuelve un error, se lo indica al cliente
                logger.error(f"Error en ESP32. Código de estado: {response.status_code}, Contenido: {response.text}")
                return JsonResponse({"success": False, "error": f"Error en ESP32: {response.text}"}, status=response.status_code)
        except json.JSONDecodeError:
            # Captura errores si el cuerpo de la petición no es un JSON válido
            return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)
        except requests.RequestException as e:
            # Captura errores de conexión o de la petición
            logger.error(f"Error de conexión al ESP32: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
        except Exception as e:
            # Captura cualquier otro error inesperado
            logger.error(f"¡Error inesperado en activar_riego_por_tiempo!: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    logger.warning(f"Intento de acceder a activar_riego_por_tiempo con método no permitido: {request.method}")
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)
# --- API para recibir la IP del ESP32 ---
@csrf_exempt
def recibir_ip_esp32(request):
    """
    Vista que recibe la IP del ESP32 vía POST desde el propio dispositivo.
    Espera un JSON como: {"ip": "192.168.20.6"}
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ip = data.get("ip")
            if not ip:
                return JsonResponse({"success": False, "error": "Falta el campo 'ip'"}, status=400)
            with open("esp32_ip.txt", "w") as f:
                f.write(ip)
            logger.info(f"IP del ESP32 registrada: {ip}")
            return JsonResponse({"success": True, "ip": ip})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)
        except Exception as e:
            logger.error(f"Error al recibir IP del ESP32: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)
