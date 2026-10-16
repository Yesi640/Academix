#!/usr/bin/env bash
# ==============================================================================
# Script de Construcción y Despliegue para ACADEMIX en la Nube (Render, Railway, etc.)
# ==============================================================================
set -o errexit

echo "==> [1/5] Actualizando gestor de paquetes pip..."
pip install --upgrade pip

echo "==> [2/5] Instalando dependencias de producción..."
pip install -r requirements.txt

echo "==> [3/5] Recopilando archivos estáticos (CSS, JS, imágenes)..."
python manage.py collectstatic --noinput

echo "==> [4/5] Aplicando migraciones de base de datos..."
python manage.py migrate

echo "==> [5/5] Inicializando datos maestros y usuarios base (Admin/Rector)..."
python manage.py setup_production_init

echo "==> Despliegue preparado exitosamente para ACADEMIX."
