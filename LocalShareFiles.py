import http.server
import socketserver
import os
import sys
import json
import webbrowser
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# =========================
# Detectar ruta base
# =========================
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

settings_path = os.path.join(base_path, "settings.json")

# =========================
# Config por defecto
# =========================
default_settings = {
    "port": 8080,
    "show_console": True
}

# Crear settings.json si no existe
if not os.path.exists(settings_path):
    with open(settings_path, "w") as f:
        json.dump(default_settings, f, indent=4)

# Cargar configuración
try:
    with open(settings_path, "r") as f:
        settings = json.load(f)
except:
    settings = default_settings

PORT = int(settings.get("port", 8080))
SHOW_CONSOLE = bool(settings.get("show_console", True))

os.chdir(base_path)

# =========================
# Handler sin spam si quieres
# =========================
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if SHOW_CONSOLE:
            super().log_message(format, *args)

# =========================
# Servidor en hilo
# =========================
httpd = None

def start_server():
    global httpd
    try:
        httpd = socketserver.TCPServer(("", PORT), CustomHandler)

        if SHOW_CONSOLE:
            print(f"Servidor en http://localhost:{PORT}")

        webbrowser.open(f"http://localhost:{PORT}")
        httpd.serve_forever()

    except OSError:
        print(f"⚠️ Puerto {PORT} ocupado. Cambia el settings.json")

def stop_server(icon=None, item=None):
    global httpd
    if httpd:
        httpd.shutdown()
    if icon:
        icon.stop()
    os._exit(0)

# =========================
# Crear icono simple
# =========================
def create_image():
    img = Image.new('RGB', (64, 64), color=(30, 30, 30))
    d = ImageDraw.Draw(img)
    d.rectangle((16, 16, 48, 48), fill=(0, 200, 255))
    return img

# =========================
# Tray icon
# =========================
def run_tray():
    icon = Icon(
        "LocalShareFiles",
        create_image(),
        "LocalShareFiles",
        menu=Menu(
            MenuItem("Abrir en navegador", lambda: webbrowser.open(f"http://localhost:{PORT}")),
            MenuItem("Salir", stop_server)
        )
    )
    icon.run()

# =========================
# Ejecutar todo
# =========================
if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    run_tray()