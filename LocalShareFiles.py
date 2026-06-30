import http.server
import socketserver
import os
import sys
import json
import webbrowser

# Detectar ruta base (compatible con PyInstaller)
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

settings_path = os.path.join(base_path, "settings.json")

# Config por defecto
default_settings = {
    "port": 8080,
    "show_console": True
}

# Crear settings.json si no existe
if not os.path.exists(settings_path):
    with open(settings_path, "w") as f:
        json.dump(default_settings, f, indent=4)

# Cargar configuración
with open(settings_path, "r") as f:
    settings = json.load(f)

PORT = settings.get("port", 8080)
SHOW_CONSOLE = settings.get("show_console", True)

# Cambiar directorio
os.chdir(base_path)

# Handler personalizado para ocultar logs si se quiere
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if SHOW_CONSOLE:
            super().log_message(format, *args)

# Iniciar servidor
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    if SHOW_CONSOLE:
        print(f"Servidor en http://localhost:{PORT}")

    # Abrir navegador automáticamente
    webbrowser.open(f"http://localhost:{PORT}")

    httpd.serve_forever()