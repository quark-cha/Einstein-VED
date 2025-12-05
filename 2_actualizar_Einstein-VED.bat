@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ====================================
echo    ACTUALIZADOR REPOSITORIO Einstein-VED
echo    Repo: quark-cha/Einstein-VED
echo ====================================
echo.

:: Verificar si Git está instalado
where git >nul 2>nul
if errorlevel 1 (
    echo ERROR: Git no está instalado o no está en el PATH
    pause
    exit /b 1
)

:: Verificar que estamos en la carpeta Einstein-VED
echo Directorio actual: %CD%
for %%i in ("%CD%") do set "CURRENT_FOLDER=%%~nxi"
if not "!CURRENT_FOLDER!"=="Einstein-VED" (
    echo ERROR: Este script debe ejecutarse desde la carpeta Einstein-VED
    echo Carpeta actual: !CURRENT_FOLDER!
    pause
    exit /b 1
)

:: Verificar si es un repositorio Git
if not exist ".git" (
    echo Inicializando repositorio Git...
    git init
    git remote add origin https://github.com/quark-cha/Einstein-VED.git
    echo ¡Repositorio Git inicializado y remote configurado!
) else (
    echo Repositorio Git encontrado.
)

:: Verificar la configuración del remote
git remote -v | findstr "quark-cha/Einstein-VED" >nul
if errorlevel 1 (
    echo Configurando remote origin...
    git remote add origin https://github.com/quark-cha/Einstein-VED.git 2>nul
    git remote set-url origin https://github.com/quark-cha/Einstein-VED.git
)

:: Obtener cambios recientes del remoto
echo.
echo Obteniendo cambios del repositorio remoto...
git fetch origin

:: Verificar estado actual
echo.
echo Estado actual del repositorio:
git status

:: Añadir todos los archivos al staging
echo.
echo Añadiendo todos los archivos al staging...
git add .

:: Verificar si hay cambios para commit
git diff --cached --quiet
if errorlevel 1 (
    echo.
    echo Haciendo commit de los cambios...
    git commit -m "Actualización automática: %date% %time%"
) else (
    echo.
    echo No hay cambios para commit.
)

:: Subir cambios al repositorio
echo.
echo Subiendo cambios a GitHub...
git push -u origin main 2>nul
if errorlevel 1 (
    git push -u origin master 2>nul
    if errorlevel 1 (
        echo Creando rama main y subiendo...
        git branch -M main
        git push -u origin main
    )
)

echo.
echo ====================================
echo         PROCESO COMPLETADO
echo ====================================
echo Repositorio: https://github.com/quark-cha/Einstein-VED
echo Última actualización: %date% %time%
echo.

:: Mostrar estado final
git status
echo.
pause