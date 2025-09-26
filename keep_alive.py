"""
🔄 Trading Analyzer Pro - Keep-Alive System
Sistema para mantener la app de Streamlit activa
"""

import requests
import time
from datetime import datetime
import threading

class StreamlitKeepAlive:
    """🔄 Sistema para mantener Streamlit Cloud activo"""
    
    def __init__(self, app_url="https://trading-analyzer-pro.streamlit.app"):
        self.app_url = app_url
        self.is_running = False
        self.ping_interval = 300  # 5 minutos
    
    def ping_app(self):
        """📡 Hacer ping a la aplicación"""
        try:
            response = requests.get(self.app_url, timeout=10)
            status = "✅ Active" if response.status_code == 200 else "⚠️ Issues"
            print(f"[{datetime.now().strftime('%H:%M:%S')}] App Status: {status} ({response.status_code})")
            return True
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Ping failed: {e}")
            return False
    
    def start_keep_alive(self):
        """🚀 Iniciar sistema keep-alive"""
        if self.is_running:
            return
        
        self.is_running = True
        print(f"🔄 Keep-Alive started for: {self.app_url}")
        
        def keep_alive_loop():
            while self.is_running:
                self.ping_app()
                time.sleep(self.ping_interval)
        
        # Ejecutar en thread separado
        thread = threading.Thread(target=keep_alive_loop, daemon=True)
        thread.start()
    
    def stop_keep_alive(self):
        """⏹️ Detener sistema keep-alive"""
        self.is_running = False
        print("⏹️ Keep-Alive stopped")

# 🌐 Sistema automático integrado en la app
def integrate_keep_alive_in_streamlit():
    """🔗 Integrar keep-alive en Streamlit (solo en producción)"""
    import os
    
    # Solo activar en Streamlit Cloud
    if os.getenv('STREAMLIT_SHARING_MODE') or 'streamlit.app' in os.getenv('URL', ''):
        keep_alive = StreamlitKeepAlive()
        keep_alive.start_keep_alive()
        return True
    return False

if __name__ == "__main__":
    # 🧪 Prueba manual
    keep_alive = StreamlitKeepAlive()
    keep_alive.start_keep_alive()
    
    try:
        # Mantener activo por 1 hora como prueba
        time.sleep(3600)
    except KeyboardInterrupt:
        keep_alive.stop_keep_alive()
        print("👋 Keep-Alive terminado")