document.addEventListener('DOMContentLoaded', function() {
    const manualSwitch = document.getElementById('manualSwitch');
    const activateTimedButton = document.getElementById('activateTimed');
    const manualDurationInput = document.getElementById('manualDuration');
    const manualStatusText = document.getElementById('manualStatus');
    const manualFeedbackDiv = document.getElementById('manualFeedback');
    const switchLabel = document.querySelector('.switch-label');

    let isRiegoManualActivo = false;

    function actualizarEstadoRiego(activo) {
        isRiegoManualActivo = activo;
        manualStatusText.textContent = activo ? 'Activo' : 'Inactivo';
        manualStatusText.className = activo ? 'activo' : 'inactivo';
        manualSwitch.checked = activo;
        switchLabel.textContent = activo ? 'Encendido' : 'Apagado';
        activateTimedButton.disabled = activo;
    }

    function mostrarMensaje(mensaje, tipo = 'info') {
        manualFeedbackDiv.textContent = mensaje;
        manualFeedbackDiv.className = `manual-feedback ${tipo}`;
        setTimeout(() => {
            manualFeedbackDiv.textContent = '';
            manualFeedbackDiv.className = 'manual-feedback';
        }, 3000);
    }

    manualSwitch.addEventListener('change', function() {
        const activar = this.checked;
        const url = activar ? '/api/riego/manual/activar/' : '/api/riego/manual/desactivar/';
        const mensajeEstado = activar ? 'activado' : 'desactivado';
        const tipoMensaje = activar ? 'success' : 'desactivado';

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                actualizarEstadoRiego(activar);
                mostrarMensaje(`Riego manual ${mensajeEstado}.`, tipoMensaje);
            } else {
                mostrarMensaje(`Error al ${mensajeEstado} el riego manual: ` + data.error, 'error');
                this.checked = !activar;
                actualizarEstadoRiego(!activar);
            }
        })
        .catch(error => {
            mostrarMensaje('Error de conexión: ' + error, 'error');
            this.checked = !activar;
            actualizarEstadoRiego(!activar);
        });
    });

    activateTimedButton.addEventListener('click', function() {
        const duracion = parseInt(manualDurationInput.value);

        if (isNaN(duracion) || duracion < 2 || duracion > 60) {
            mostrarMensaje("Duración inválida. Debe estar entre 2 y 60 segundos.", 'error');
            return;
        }

        fetch('/api/riego/manual/activar_por_tiempo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ duration: duracion })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                actualizarEstadoRiego(true);
                mostrarMensaje(`Riego manual activado por ${duracion} segundos.`, 'success');
                setTimeout(() => {
                    actualizarEstadoRiego(false);
                }, duracion * 1000);
            } else {
                mostrarMensaje(`Error al activar por duración: ` + data.error, 'error');
            }
        })
        .catch(error => {
            mostrarMensaje('Error de conexión: ' + error, 'error');
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
document.getElementById('obtenerIPBtn').addEventListener('click', async function () {
    try {
        const response = await fetch('/obtener_ip/');
        const data = await response.json();
        document.getElementById('ipValor').textContent = data.ip;
        console.log("✅ IP obtenida:", data.ip);
    } catch (error) {
        console.error("❌ Error al obtener IP:", error);
        document.getElementById('ipValor').textContent = "Error al obtener IP";
    }
});
