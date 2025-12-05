@echo off
setlocal ENABLEDELAYEDEXPANSION

echo ================================================
echo   BACKUP + LIMPIEZA + COMMIT + PUSH A GITHUB
echo ================================================
echo Directorio del proyecto:
echo %CD%
echo.

REM =============================
REM 1. ELIMINAR LOGS DE MANERA SEGURA
REM =============================
echo Eliminando archivos .log locales...
del /s *.log 2>nul

REM =============================
REM 2. CREAR BACKUP EN ZIP
REM =============================
echo Creando backup...

set FECHA=%DATE:~-4%-%DATE:~3,2%-%DATE:~0,2%
set HORA=%TIME:~0,2%-%TIME:~3,2%
set HORA=%HORA: =0%

set BACKUPNAME=backup_%FECHA%_%HORA%.zip

REM Crear carpeta Backups si no existe
if not exist "Backups" mkdir Backups

powershell -command "Compress-Archive -Path * -DestinationPath 'Backups\\%BACKUPNAME%' -Force"

echo Backup creado: Backups\%BACKUPNAME%
echo.

REM =============================
REM 3. COMPROBAR SI HAY CAMBIOS
REM =============================
echo Comprobando si hay cambios para subir...
git status --porcelain > temp_git_status.txt

set /p HASCHANGES=<temp_git_status.txt
del temp_git_status.txt

if "!HASCHANGES!"=="" (
    echo No hay cambios para subir. Nada que hacer.
    echo (Backup ya creado de todas formas)
    pause
    exit /b
)

REM =============================
REM 4. AGREGAR Y COMMIT SOLO SI HAY CAMBIOS
REM =============================
echo Cambios detectados. Realizando commit...
git add .

REM Crear mensaje de commit automático
set MSG="Auto-update %FECHA% %HORA%"
git commit -m %MSG%

REM =============================
REM 5. COMPROBAR REMOTO
REM =============================
echo Verificando repositorio remoto...
git remote get-url origin >nul 2>&1

if %ERRORLEVEL% NEQ 0 (
    echo No se encontro remoto configurado.
    echo Pegue la URL del repositorio (.git):
    set /p repoUrl=
    git remote add origin %repoUrl%
)

REM =============================
REM 6. HACER PUSH
REM =============================
echo Subiendo cambios a GitHub...
git push

echo ================================================
echo       PROYECTO RESPALDADO Y ACTUALIZADO
echo ================================================
pause
