# 🎵 HomePod Windows - AirPlay Streamer

Aplicación para usar un HomePod mini como altavoz de tu ordenador Windows.

## ✨ Características

✅ Descubrimiento automático de dispositivos HomePod  
✅ Interfaz gráfica intuitiva con Tkinter  
✅ Streaming de audio del sistema  
✅ Control de volumen  
✅ Panel de información en tiempo real  
✅ Manejo de errores y logs  

## 🚀 Instalación

1. **Clona el repositorio**
```bash
git clone https://github.com/GonzaloCardona/test-copilot-homepod.git
cd test-copilot-homepod
```

2. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuración Previa (Importante)

### Windows 10/11 - Habilitar Stereo Mix

1. Click derecho en el icono de volumen (esquina inferior derecha)
2. Selecciona "Sonidos"
3. Ve a la pestaña "Grabar"
4. Click derecho en la ventana vacía
5. Marca "Mostrar dispositivos deshabilitados"
6. Busca "Stereo Mix" y haz click derecho
7. Selecciona "Habilitar"
8. Haz click derecho nuevamente y selecciona "Establecer como dispositivo predeterminado"

## ▶️ Uso

```bash
python main.py
```

### Pasos de Uso:

1. **Abre la aplicación**: Se mostrará una lista de dispositivos disponibles
2. **Selecciona tu HomePod**: Haz click en el dispositivo de la lista
3. **Conecta**: Click en el botón "🔌 Conectar"
4. **Inicia streaming**: Click en "▶️ Iniciar Stream"
5. **Ajusta volumen**: Usa el slider de volumen
6. **Detén**: Click en "⏹️ Detener Stream" o "❌ Desconectar"

## 📁 Estructura del Proyecto

```
├── main.py                    # Punto de entrada
├── requirements.txt           # Dependencias
├── core/
│   ├── __init__.py
│   ├── device_discovery.py   # Descubrimiento de dispositivos (mDNS)
│   ├── audio_handler.py      # Captura de audio del sistema
│   └── airplay.py            # Controlador AirPlay
└── ui/
    ├── __init__.py
    └── main_window.py        # Interfaz gráfica principal
```

## 🔧 Dependencias

- **zeroconf**: Para descubrimiento de dispositivos (mDNS/Bonjour)
- **pyaudio**: Para capturar audio del sistema
- **tkinter**: Interfaz gráfica (incluido en Python)

## 🐛 Solución de Problemas

### "No se encuentran dispositivos"
- Verifica que tu HomePod esté conectado a la misma red Wi-Fi
- Comprueba que el HomePod esté encendido
- Intenta reiniciar el HomePod

### "Error de conexión"
- Verifica la dirección IP del HomePod
- Comprueba la conectividad de red
- Intenta desconectar y conectar de nuevo

### "Sin audio"
- Verifica que Stereo Mix esté habilitado en Windows
- Comprueba que PyAudio haya detectado los dispositivos correctamente
- Asegúrate de que el volumen del sistema no esté al mínimo

## 📝 Logs

La aplicación registra todos los eventos en la consola. Busca mensajes de error si algo no funciona correctamente.

## 🎯 Mejoras Futuras

- [ ] Visualizador de audio
- [ ] Historial de dispositivos
- [ ] Perfiles de sonido personalizados
- [ ] Grabación de sesiones
- [ ] Soporte para múltiples dispositivos simultáneamente

## 📄 Licencia

Este proyecto está bajo licencia MIT.

## 👨‍💻 Autor

GonzaloCardona
