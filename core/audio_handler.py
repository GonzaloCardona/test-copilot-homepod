import pyaudio
import threading
import logging

logger = logging.getLogger(__name__)

class AudioHandler:
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.audio_buffer = []
        
    def get_devices(self):
        """Obtiene lista de dispositivos de audio disponibles"""
        devices = []
        for i in range(self.pa.get_device_count()):
            info = self.pa.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                devices.append({
                    'id': i,
                    'name': info['name'],
                    'channels': info['maxInputChannels']
                })
        return devices
    
    def start_recording(self, device_id=None, callback=None):
        """Inicia la grabación de audio del sistema"""
        try:
            # Usa Stereo Mix por defecto
            if device_id is None:
                device_id = self._find_stereo_mix()
            
            self.stream = self.pa.open(
                format=pyaudio.paFloat32,
                channels=2,
                rate=44100,
                input=True,
                input_device_index=device_id,
                frames_per_buffer=1024
            )
            
            self.is_recording = True
            logger.info(f"Grabación iniciada desde dispositivo {device_id}")
            
            # Thread de grabación
            def record():
                while self.is_recording:
                    try:
                        data = self.stream.read(1024, exception_on_overflow=False)
                        if callback:
                            callback(data)
                    except Exception as e:
                        logger.error(f"Error grabando: {e}")
            
            threading.Thread(target=record, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Error iniciando grabación: {e}")
    
    def stop_recording(self):
        """Detiene la grabación"""
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        logger.info("Grabación detenida")
    
    def _find_stereo_mix(self):
        """Busca el dispositivo 'Stereo Mix'"""
        for i in range(self.pa.get_device_count()):
            info = self.pa.get_device_info_by_index(i)
            if 'stereo mix' in info['name'].lower():
                return i
        return 0  # Por defecto, usa el primer dispositivo
    
    def cleanup(self):
        """Limpia recursos"""
        self.stop_recording()
        self.pa.terminate()