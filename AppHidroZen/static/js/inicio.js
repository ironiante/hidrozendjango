const canvas = document.getElementById("particleCanvas");
const ctx = canvas.getContext("2d");
const progressBar = document.getElementById('progressBar');
const progressValue = document.getElementById('progressValue');
const progressFill = document.getElementById('progressFill');
const programButton = document.getElementById('programButton');
const modal = document.getElementById('modal');
const modalMessage = document.getElementById('modalMessage');
const closeButton = document.getElementById('closeButton');
const datePicker = document.getElementById('datePicker');
const timePicker = document.getElementById('timePicker');
const durationSlider = document.getElementById('durationSlider');
const durationValue = document.getElementById('durationValue');

// Ajustar tamaño del canvas
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Mostrar valor de humedad en tiempo real
progressBar.addEventListener('input', function () {
    const value = progressBar.value;
    progressValue.textContent = `${value}%`;
    progressFill.style.width = `${value}%`;
});

// Mostrar valor de duración en tiempo real
durationSlider.addEventListener('input', function () {
    durationValue.textContent = durationSlider.value;
});

// Función para mostrar el modal
function mostrarModal(mensaje) {
    modalMessage.textContent = mensaje;
    modal.style.display = 'flex';
}
//const esp32IP = "http://192.168.20.7";

// Obtener IP del ESP32 desde Django
async function obtenerIPESP32() {
    try {
        const response = await fetch('/obtener_ip/');
        const data = await response.json();
        return data.ip; // Devuelve la IP como 'http://192.168.x.x'
    } catch (error) {
        console.error("Error obteniendo la IP del ESP32:", error);
        return null;
    }
}

// Botón de programar
programButton.addEventListener('click', async function () {
    const threshold = Number(progressBar.value);       // humedad seleccionada
    const date = datePicker.value;
    const time = timePicker.value;
    const duration = durationSlider.value;

    // 1) Obtener la humedad del sensor desde Django
    let sensorHumedad = 0;
    try {
        const res = await fetch('/api/humedad/');
        const json = await res.json();
        sensorHumedad = Number(json.humedad);
    } catch (e) {
        console.error("No se pudo obtener humedad del sensor:", e);
        mostrarModal("Error al obtener humedad actual. Intenta de nuevo.");
        return;
    }

    // 2) Comparar con el umbral
    if (sensorHumedad >= threshold) {
        mostrarModal(`🌱 La humedad actual es ${sensorHumedad}%, por encima del umbral (${threshold}%). No es necesario regar.`);
        return;  // Salimos sin programar el riego
    }

    // 3) Si llegamos aquí, la humedad está por debajo del umbral, procedemos
    const ip = await obtenerIPESP32();
    if (!ip) {
        mostrarModal("❌ No se pudo obtener la IP del ESP32.");
        return;
    }

    const timestamp = Date.now();
    // Enviar duración
    await fetch(`${ip}/set-duracion?segundos=${duration}&_=${timestamp}`)
    .catch(err => console.error("Error en set-duración:", err));
    // Enviar programación
    fetch(`${ip}/programar?humedad=${threshold}&fecha=${date}&hora=${time}&_=${timestamp}`)
        .then(r => r.text())
        .then(msg => mostrarModal(msg))
        .catch(err => {
            console.error("Error al programar:", err);
            mostrarModal("Error al conectar con la ESP32.");
        });
});


// Botón cerrar modal
closeButton.addEventListener('click', function () {
    modal.style.display = 'none';
});

// Animación de partículas
let particles = [];
for (let i = 0; i < 50; i++) {
    particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 4 + 1.5,
        speedX: Math.random() * 1.5 - 0.75,
        speedY: Math.random() * 1.5 - 0.75,
        color: "rgba(30, 144, 255, 0.7)"
    });
}

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
        ctx.beginPath();
        ctx.fillStyle = p.color;
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fill();

        p.x += p.speedX;
        p.y += p.speedY;

        if (p.x < 0 || p.x > canvas.width) p.speedX *= -1;
        if (p.y < 0 || p.y > canvas.height) p.speedY *= -1;
    });
    requestAnimationFrame(animateParticles);
}
animateParticles();

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



