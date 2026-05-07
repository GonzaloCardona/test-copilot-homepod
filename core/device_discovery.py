import threading
import logging
from zeroconf import ServiceBrowser, Zeroconf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeviceDiscovery:
    def __init__(self, callback=None):
        self.zeroconf = Zeroconf()
        self.devices = {}
        self.callback = callback
        self.service_browser = None
        
    def start_discovery(self):
        """Inicia el descubrimiento de dispositivos AirPlay"""
        try:
            self.service_browser = ServiceBrowser(
                self.zeroconf,
                "_airplay._tcp.local.",
                handlers=[self._on_service_state_change]
            )
            logger.info("Descubrimiento de dispositivos iniciado")
        except Exception as e:
            logger.error(f"Error en descubrimiento: {e}")
    
    def _on_service_state_change(self, zeroconf, service_type, name, state_change):
        """Maneja cambios en los servicios descubiertos"""
        from zeroconf import ServiceStateChange
        
        if state_change == ServiceStateChange.Added:
            self._add_device(zeroconf, name)
        elif state_change == ServiceStateChange.Removed:
            self._remove_device(name)
    
    def _add_device(self, zeroconf, name):
        """Agrega un nuevo dispositivo encontrado"""
        try:
            info = zeroconf.get_service_info(
                "_airplay._tcp.local.", name
            )
            if info:
                device_name = name.replace("._airplay._tcp.local.", "")
                address = str(info.addresses[0]) if info.addresses else "Desconocida"
                port = info.port
                
                self.devices[device_name] = {
                    'name': device_name,
                    'address': address,
                    'port': port,
                    'service_name': name
                }
                
                logger.info(f"Dispositivo encontrado: {device_name} ({address}:{port})")
                if self.callback:
                    self.callback('added', device_name, self.devices[device_name])
        except Exception as e:
            logger.error(f"Error al agregar dispositivo: {e}")
    
    def _remove_device(self, name):
        """Remueve un dispositivo"""
        device_name = name.replace("._airplay._tcp.local.", "")
        if device_name in self.devices:
            del self.devices[device_name]
            logger.info(f"Dispositivo removido: {device_name}")
            if self.callback:
                self.callback('removed', device_name, None)
    
    def get_devices(self):
        """Retorna lista de dispositivos disponibles"""
        return list(self.devices.values())
    
    def stop_discovery(self):
        """Detiene el descubrimiento"""
        if self.zeroconf:
            self.zeroconf.close()