import tkinter as tk
from tkinter import ttk, messagebox
import threading
import logging
from core.device_discovery import DeviceDiscovery
from core.audio_handler import AudioHandler
from core.airplay import AirPlayController

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("HomePod Windows - AirPlay Streamer")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.device_discovery = DeviceDiscovery(callback=self._on_device_change)
        self.audio_handler = AudioHandler()
        self.airplay_controller = None
        self.is_streaming = False
        self.selected_device = None
        
        # Inicia descubrimiento en thread
        threading.Thread(target=self.device_discovery.start_discovery, daemon=True).start()
        
        self._setup_ui()
        self._start_device_refresh()
    
    def _setup_ui(self):
        """Configura la interfaz gráfica"""
        
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X)
        
        title = tk.Label(
            header,
            text="🎵 HomePod Windows",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title.pack(pady=15)
        
        # Frame de dispositivos
        devices_frame = tk.LabelFrame(
            self.root,
            text="Dispositivos Disponibles",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        devices_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Listbox de dispositivos
        self.devices_listbox = tk.Listbox(
            devices_frame,
            height=8,
            font=("Arial", 10),
            selectmode=tk.SINGLE,
            bg="white",
            border=1
        )
        self.devices_listbox.pack(fill=tk.BOTH, expand=True)
        self.devices_listbox.bind("<<ListboxSelect>>", self._on_device_select)
        
        scrollbar = ttk.Scrollbar(devices_frame, orient=tk.VERTICAL, command=self.devices_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.devices_listbox.config(yscrollcommand=scrollbar.set)
        
        # Frame de controles
        controls_frame = tk.Frame(self.root, bg="#f0f0f0")
        controls_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Botones principales
        self.connect_btn = tk.Button(
            controls_frame,
            text="🔌 Conectar",
            command=self._connect_device,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            state=tk.DISABLED,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        self.stream_btn = tk.Button(
            controls_frame,
            text="▶️ Iniciar Stream",
            command=self._toggle_stream,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            state=tk.DISABLED,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.stream_btn.pack(side=tk.LEFT, padx=5)
        
        disconnect_btn = tk.Button(
            controls_frame,
            text="❌ Desconectar",
            command=self._disconnect_device,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        disconnect_btn.pack(side=tk.LEFT, padx=5)
        
        # Control de volumen
        volume_frame = tk.Frame(self.root, bg="#f0f0f0")
        volume_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(volume_frame, text="Volumen:", bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.volume_slider = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self._set_volume,
            bg="#ecf0f1",
            fg="#2c3e50",
            state=tk.DISABLED,
            length=300
        )
        self.volume_slider.set(50)
        self.volume_slider.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.volume_label = tk.Label(volume_frame, text="50%", bg="#f0f0f0", font=("Arial", 10))
        self.volume_label.pack(side=tk.LEFT)
        
        # Panel de información
        info_frame = tk.LabelFrame(
            self.root,
            text="Información",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        info_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.info_label = tk.Label(
            info_frame,
            text="Estado: Esperando...",
            bg="#f0f0f0",
            font=("Arial", 9),
            justify=tk.LEFT
        )
        self.info_label.pack(anchor=tk.W)
    
    def _on_device_change(self, action, device_name, device_info):
        """Callback cuando cambia la lista de dispositivos"""
        self.root.after(0, self._refresh_device_list)
    
    def _refresh_device_list(self):
        """Actualiza la lista de dispositivos"""
        self.devices_listbox.delete(0, tk.END)
        devices = self.device_discovery.get_devices()
        
        if not devices:
            self.devices_listbox.insert(tk.END, "⏳ Buscando dispositivos...")
        else:
            for device in devices:
                self.devices_listbox.insert(
                    tk.END,
                    f"🔊 {device['name']} ({device['address']})"
                )
    
    def _on_device_select(self, event):
        """Cuando se selecciona un dispositivo"""
        selection = self.devices_listbox.curselection()
        if selection:
            devices = self.device_discovery.get_devices()
            self.selected_device = devices[selection[0]]
            self.connect_btn.config(state=tk.NORMAL)
            self._update_info(f"Dispositivo seleccionado: {self.selected_device['name']}")
    
    def _connect_device(self):
        """Conecta al dispositivo seleccionado"""
        if not self.selected_device:
            messagebox.showwarning("Advertencia", "Por favor selecciona un dispositivo")
            return
        
        try:
            self.airplay_controller = AirPlayController(
                self.selected_device['address'],
                self.selected_device['port']
            )
            
            if self.airplay_controller.connect():
                self.stream_btn.config(state=tk.NORMAL)
                self.volume_slider.config(state=tk.NORMAL)
                self._update_info(f"✅ Conectado a: {self.selected_device['name']}")
                messagebox.showinfo("Éxito", f"Conectado a {self.selected_device['name']}")
            else:
                self._update_info("❌ No se pudo conectar")
                messagebox.showerror("Error", "No se pudo conectar al dispositivo")
        except Exception as e:
            logger.error(f"Error conectando: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def _toggle_stream(self):
        """Inicia o detiene el stream de audio"""
        if not self.is_streaming:
            self._start_stream()
        else:
            self._stop_stream()
    
    def _start_stream(self):
        """Inicia el streaming"""
        try:
            def audio_callback(data):
                if self.airplay_controller:
                    self.airplay_controller.send_audio(data)
            
            self.audio_handler.start_recording(callback=audio_callback)
            self.is_streaming = True
            self.stream_btn.config(text="⏹️ Detener Stream", bg="#e74c3c")
            self._update_info("🎵 Streaming en vivo...")
            logger.info("Stream iniciado")
        except Exception as e:
            logger.error(f"Error iniciando stream: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def _stop_stream(self):
        """Detiene el streaming"""
        try:
            self.audio_handler.stop_recording()
            self.is_streaming = False
            self.stream_btn.config(text="▶️ Iniciar Stream", bg="#3498db")
            self._update_info("Stream detenido")
            logger.info("Stream detenido")
        except Exception as e:
            logger.error(f"Error deteniendo stream: {e}")
    
    def _disconnect_device(self):
        """Desconecta del dispositivo"""
        if self.is_streaming:
            self._stop_stream()
        
        if self.airplay_controller:
            self.airplay_controller.disconnect()
        
        self.airplay_controller = None
        self.selected_device = None
        self.stream_btn.config(state=tk.DISABLED)
        self.volume_slider.config(state=tk.DISABLED)
        self.connect_btn.config(state=tk.DISABLED)
        self._update_info("Desconectado")
    
    def _set_volume(self, value):
        """Establece el volumen"""
        self.volume_label.config(text=f"{value}%")
        if self.airplay_controller:
            self.airplay_controller.set_volume(int(value))
    
    def _update_info(self, message):
        """Actualiza el panel de información"""
        self.info_label.config(text=f"Estado: {message}")
    
    def _start_device_refresh(self):
        """Refresca la lista de dispositivos periódicamente"""
        def refresh():
            import time
            while True:
                time.sleep(5)
                self._refresh_device_list()
        
        threading.Thread(target=refresh, daemon=True).start()