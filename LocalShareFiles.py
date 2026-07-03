import os
import sys
import json
import webbrowser
import threading
import subprocess
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
    "port": 4934,
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

PORT = int(settings.get("port", 4934))
SHOW_CONSOLE = bool(settings.get("show_console", True))

os.chdir(base_path)

# =========================
# PROCESO DEL SERVIDOR
# =========================
http_process = None

def start_server():
    global http_process
    try:
        http_process = subprocess.Popen(
            ["python3", "-m", "http.server", str(PORT)],
            cwd=base_path
        )

        if SHOW_CONSOLE:
            print(f"Servidor en http://localhost:{PORT}")

        webbrowser.open(f"http://localhost:{PORT}")

    except Exception as e:
        print("Error iniciando servidor:", e)

# =========================
# Cerrar correctamente
# =========================
def exit_app(icon, item):
    global http_process

    if http_process:
        http_process.terminate()
        http_process.wait()

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
    start_server()
    run_tray()