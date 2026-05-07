import socket
import struct
import logging
import base64

logger = logging.getLogger(__name__)

class AirPlayController:
    def __init__(self, host, port=5000):
        self.host = host
        self.port = port
        self.socket = None
        
    def connect(self):
        """Conecta al dispositivo AirPlay"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            logger.info(f"Conectado a {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Error conectando a AirPlay: {e}")
            return False
    
    def send_audio(self, audio_data):
        """Envía datos de audio al dispositivo"""
        try:
            if not self.socket:
                return False
            
            # Formato simple de envío
            header = struct.pack('>I', len(audio_data))
            self.socket.sendall(header + audio_data)
            return True
        except Exception as e:
            logger.error(f"Error enviando audio: {e}")
            return False
    
    def set_volume(self, volume):
        """Establece el volumen (0-100)"""
        try:
            # Comando RTSP para volumen
            volume_db = -30 + (volume / 100) * 30
            command = f"SET_PARAMETER rtsp://{self.host}/audio HTTP/1.1\r\nContent-Type: text/parameters\r\nContent-Length: 15\r\n\r\nvolume: {volume_db}\r\n"
            if self.socket:
                self.socket.sendall(command.encode())
            logger.info(f"Volumen establecido a {volume}%")
            return True
        except Exception as e:
            logger.error(f"Error estableciendo volumen: {e}")
            return False
    
    def disconnect(self):
        """Desconecta del dispositivo"""
        try:
            if self.socket:
                self.socket.close()
            logger.info("Desconectado de AirPlay")
        except Exception as e:
            logger.error(f"Error desconectando: {e}")