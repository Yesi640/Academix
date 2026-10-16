@echo off
:: ============================================================================
:: SCRIPT DE RESPALDO AUTOMATIZADO - SISTEMA ACADEMIX
:: Programa ADSO - SENA | Evidencia RAP: Continuidad y Mantenimiento TI
:: ============================================================================
:: Este script está diseñado para ejecutarse diariamente de forma automática
:: a través del Programador de Tareas de Windows (Task Scheduler).
:: Realiza copia consistente de la base de datos, sincronización incremental
:: de archivos multimedia y copia del entorno (.env).
:: ============================================================================

setlocal enabledelayedexpansion

:: 1. Definir rutas de origen y destino
set ORIGEN_PROYECTO=C:\Academix
set RUTA_DESTINO=C:\Academix_Backups

:: Obtener fecha actual en formato YYYY-MM-DD
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set DATETIME=%%I
set FECHA=%DATETIME:~0,4%-%DATETIME:~4,2%-%DATETIME:~6,2%
set HORA=%DATETIME:~8,2%-%DATETIME:~10,2%

set CARPETA_HOY=%RUTA_DESTINO%\%FECHA%
set LOG_FILE=%RUTA_DESTINO%\respaldos_log.txt

if not exist "%RUTA_DESTINO%" mkdir "%RUTA_DESTINO%"
if not exist "%CARPETA_HOY%" mkdir "%CARPETA_HOY%"

echo ======================================================= >> "%LOG_FILE%"
echo [%FECHA% %HORA%] INICIANDO RESPALDO AUTOMATICO ACADEMIX >> "%LOG_FILE%"

:: 2. Respaldo de Base de Datos SQLite (Copia consistente)
if exist "%ORIGEN_PROYECTO%\db.sqlite3" (
    copy "%ORIGEN_PROYECTO%\db.sqlite3" "%CARPETA_HOY%\academix_db_%FECHA%.sqlite3" /Y >nul
    echo [%FECHA% %HORA%] [OK] Base de datos respaldada correctamente. >> "%LOG_FILE%"
) else (
    echo [%FECHA% %HORA%] [ALERTA] No se encontro db.sqlite3 en el origen. >> "%LOG_FILE%"
)

:: 3. Respaldo Incremental de Archivos Multimedia (Fotos de expedientes, certificados)
:: Utiliza ROBOCOPY con /XO para copiar únicamente archivos nuevos o modificados
if exist "%ORIGEN_PROYECTO%\media" (
    robocopy "%ORIGEN_PROYECTO%\media" "%CARPETA_HOY%\media" /E /XO /R:2 /W:3 >nul
    echo [%FECHA% %HORA%] [OK] Carpeta media sincronizada de forma incremental. >> "%LOG_FILE%"
) else (
    echo [%FECHA% %HORA%] [INFO] Carpeta media no requiere sincronizacion. >> "%LOG_FILE%"
)

:: 4. Respaldo de configuracion (.env)
if exist "%ORIGEN_PROYECTO%\.env" (
    copy "%ORIGEN_PROYECTO%\.env" "%CARPETA_HOY%\env_config_%FECHA%.bak" /Y >nul
    echo [%FECHA% %HORA%] [OK] Archivo de configuracion .env respaldado. >> "%LOG_FILE%"
)

echo [%FECHA% %HORA%] RESPALDO FINALIZADO EXITOSAMENTE. >> "%LOG_FILE%"
echo ======================================================= >> "%LOG_FILE%"

exit /b 0
