import http.server
import socketserver
import os
import sys
import json
import webbrowser
import threading
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# Detectar si hay terminal
if not sys.stdout.isatty():
    print("This program must be run from a terminal.")
    sys.exit(1)
    
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

# =========================
# Crear settings y salir
# =========================
if not os.path.exists(settings_path):
    with open(settings_path, "w") as f:
        json.dump(default_settings, f, indent=4)

    print("Se ha creado settings.json. Configúralo y vuelve a ejecutar.")
    input("Pulsa ENTER para salir...")
    sys.exit(0)

# =========================
# Cargar configuración
# =========================
try:
    with open(settings_path, "r") as f:
        settings = json.load(f)
except:
    print("Error leyendo settings.json")
    sys.exit(1)

PORT = int(settings.get("port", 8080))
SHOW_CONSOLE = bool(settings.get("show_console", True))

os.chdir(base_path)

# =========================
# Handler
# =========================
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if SHOW_CONSOLE:
            super().log_message(format, *args)

# =========================
# Servidor
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

# =========================
# Cerrar servidor correctamente
# =========================
def exit_app(icon, item):
    global httpd
    if httpd:
        httpd.shutdown()
        httpd.server_close()
    icon.stop()
    sys.exit(0)

# =========================
# Abrir navegador
# =========================
def open_browser(icon, item):
    webbrowser.open(f"http://localhost:{PORT}")

# =========================
# Icono simple
# =========================
def create_image():
    img = Image.new('RGB', (64, 64), (30, 30, 30))
    d = ImageDraw.Draw(img)
    d.rectangle((16, 16, 48, 48), fill=(0, 200, 255))
    return img

# =========================
# Tray
# =========================
def run_tray():
    icon = Icon(
        "LocalShareFiles",
        create_image(),
        "LocalShareFiles",
        menu=Menu(
            MenuItem("Abrir en navegador", open_browser),
            MenuItem("Salir", exit_app)
        )
    )
    icon.run()

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    run_tray()