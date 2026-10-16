#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
iniciar_servidor_produccion.py
==============================
Lanzador de PRODUCCION para ACADEMIX usando Waitress (WSGI Server profesional)
y WhiteNoise (Entrega de estilos CSS, Javascript e imagenes en produccion).

Uso:
    python iniciar_servidor_produccion.py           # Puerto 8000
    python iniciar_servidor_produccion.py 8080      # Puerto personalizado
"""

import os
import sys
import socket
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

os.chdir(BASE_DIR)
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


def get_network_ips():
    """Detecta las IPs activas de la maquina en la red local."""
    ips = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith("127."):
            ips.append(ip)
    except Exception:
        pass
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith("127.") and not ip.startswith("169.254.") and ip not in ips:
                ips.append(ip)
    except Exception:
        pass
    return ips


def print_banner(ips, port, threads):
    width = 74
    print("=" * width)
    print("   ACADEMIX - SERVIDOR DE PRODUCCION (Waitress WSGI)".center(width))
    print("   Sistema de Gestion Academica y Control Escolar".center(width))
    print("=" * width)
    print()
    print(f"  [OK] Servidor     : Waitress {threads} hilos - Modo Produccion Seguro")
    print(f"  [OK] Estilos CSS  : WhiteNoise activo (Archivos estaticos integrados)")
    print(f"  [OK] Escuchando   : 0.0.0.0:{port}")
    print()
    print("  [1] ACCESO DESDE ESTE COMPUTADOR:")
    print(f"      -> Abrir en Google Chrome o Edge:  http://localhost:{port}/")
    print(f"      -> O tambien:                      http://127.0.0.1:{port}/")
    print()
    print("  [2] ACCESO DESDE OTROS DISPOSITIVOS EN LA RED (Mobiles, Tablets, PCs):")
    if ips:
        for ip in ips:
            print(f"      -> http://{ip}:{port}/")
    else:
        print("      [!] No se detecto IP de red activa.")
    print()
    print("  [i] Presione Ctrl + C en esta ventana para detener el servidor.")
    print("=" * width)
    print()


def main():
    port = 8000
    threads = 8

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    try:
        from waitress import serve
    except ImportError:
        print("\n[ERROR] Waitress no esta instalado.")
        print("        Ejecute: pip install waitress")
        sys.exit(1)

    env_file = BASE_DIR / '.env'
    if not env_file.exists():
        print("\n[ERROR] No se encontro el archivo .env")
        print("        Copie .env.example como .env y configure los valores.")
        sys.exit(1)

    from dotenv import load_dotenv
    load_dotenv(env_file)

    try:
        from config.wsgi import application
        # Envoltura con WhiteNoise para servir CSS, JS e imagenes con diseno 100% perfecto
        try:
            from whitenoise import WhiteNoise
            staticfiles_dir = BASE_DIR / 'staticfiles'
            if not staticfiles_dir.exists():
                staticfiles_dir.mkdir(parents=True, exist_ok=True)
            application = WhiteNoise(application, root=str(staticfiles_dir), prefix='/static/')
            static_dir = BASE_DIR / 'static'
            if static_dir.exists():
                application.add_files(str(static_dir), prefix='/static/')
        except Exception as e:
            print(f"  [AVISO] Advertencia WhiteNoise: {e}")
    except Exception as e:
        print(f"\n[ERROR] No se pudo cargar Django: {e}")
        sys.exit(1)

    ips = get_network_ips()
    print_banner(ips, port, threads)

    try:
        serve(
            application,
            host='0.0.0.0',
            port=port,
            threads=threads,
            channel_timeout=120,
            cleanup_interval=30,
            connection_limit=500,
        )
    except KeyboardInterrupt:
        print("\n\n[INFO] Servidor ACADEMIX detenido correctamente.")
    except OSError as e:
        print(f"\n[ERROR] Puerto {port} no disponible: {e}")
        print(f"        Intente: python iniciar_servidor_produccion.py 8080")


if __name__ == '__main__':
    main()
