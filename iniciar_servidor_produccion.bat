@echo off
chcp 65001 > nul
title ACADEMIX - Servidor de Produccion (Waitress)

echo.
echo  =====================================================================
echo    ACADEMIX - INICIANDO SERVIDOR DE PRODUCCION
echo  =====================================================================
echo.

:: Ir a la carpeta del proyecto
cd /d "%~dp0"

:: Verificar si existe el entorno virtual
if exist "venv\Scripts\python.exe" (
    echo  [OK] Entorno virtual encontrado.
    set PYTHON=venv\Scripts\python.exe
) else (
    echo  [WARN] Entorno virtual no encontrado. Usando Python del sistema.
    set PYTHON=python
)

:: Verificar si existe el archivo de configuracion
if not exist ".env" (
    echo.
    echo  [ERROR] No se encontro el archivo .env
    echo          Copie el archivo .env.example como .env y configure los valores.
    echo.
    pause
    exit /b 1
)

:: Verificar si waitress esta instalado
%PYTHON% -c "import waitress" 2>nul
if errorlevel 1 (
    echo  [INFO] Instalando servidor Waitress...
    %PYTHON% -m pip install waitress
)

echo  [OK] Iniciando servidor de produccion...
echo.

:: Lanzar el servidor de produccion
%PYTHON% iniciar_servidor_produccion.py %1

echo.
echo  [INFO] Servidor detenido.
pause
