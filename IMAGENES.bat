@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ====================================
echo Procesador de archivos .py
echo ====================================

:: Cambiar al directorio .\tools
cd /d "%~dp0tools" 2>nul
if errorlevel 1 (
    echo Error: No se pudo acceder al directorio .\tools
    pause
    exit /b 1
)

echo Directorio actual: %cd%
echo.

:: Verificar si existe el directorio ..\src
if not exist "..\src" (
    echo Error: No se encuentra el directorio ..\src
    pause
    exit /b 1
)

:: Menú de idiomas
echo Seleccione el idioma:
echo 1. English (en)
echo 2. Français (fr)
echo 3. Italiano (it)
echo 4. Slovenčina (sk)
echo 5. 中文 (zh)
echo.

set /p opcion="Ingrese el número del idioma (1-5): "

:: Mapear opción a código de idioma
if "%opcion%"=="1" set idioma=en
if "%opcion%"=="2" set idioma=fr
if "%opcion%"=="3" set idioma=it
if "%opcion%"=="4" set idioma=sk
if "%opcion%"=="5" set idioma=zh

if not defined idioma (
    echo Opción inválida
    pause
    exit /b 1
)

echo Usando idioma: %idioma%
echo.

:: Contadores
set contador=0
set procesados=0
set errores=0

:: Procesar cada archivo .py en ..\src
echo Buscando archivos .py en ..\src...
echo.

for /r "..\src" %%f in (*.py) do (
    set /a contador+=1
    echo [%contador%] Procesando: %%~nxf
    
    :: Ejecutar python explorar.py con el archivo y idioma
    python explorar.py "%%f" %idioma%
    
    if errorlevel 1 (
        echo ERROR al procesar: %%~nxf
        set /a errores+=1
    ) else (
        echo OK: %%~nxf procesado correctamente
        set /a procesados+=1
    )
    echo.
)

echo ====================================
echo RESUMEN:
echo Total archivos encontrados: %contador%
echo Archivos procesados: %procesados%
echo Archivos con errores: %errores%
echo Idioma utilizado: %idioma%
echo ====================================
echo.

if %errores% gtr 0 (
    echo Algunos archivos tuvieron errores. Revise los mensajes arriba.
) else (
    echo Todos los archivos procesados exitosamente.
)

pause