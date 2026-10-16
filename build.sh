#!/usr/bin/env bash
# ==============================================================================
# Script de Construcción y Despliegue para ACADEMIX en la Nube (Render, Railway, etc.)
# ==============================================================================
set -o errexit

echo "==> [1/4] Actualizando gestor de paquetes pip..."
pip install --upgrade pip

echo "==> [2/4] Instalando dependencias de producción..."
pip install -r requirements.txt

echo "==> [3/4] Recopilando archivos estáticos (CSS, JS, imágenes)..."
python manage.py collectstatic --noinput

echo "==> [4/4] Aplicando migraciones de base de datos..."
python manage.py migrate

echo "==> Despliegue preparado exitosamente para ACADEMIX."
