@echo off
chcp 65001 >nul 2>&1
cd /d "C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED"
title GIT MAINTENANCE - EINSTEIN-VED
color 0A

:menu
cls
echo ========================================
echo    GIT MAINTENANCE - EINSTEIN-VED
echo ========================================
echo.
echo [1] SUBIR CAMBIOS (commit + push)
echo [2] VER ESTADO
echo [3] VER HISTORIAL
echo [4] SALIR
echo.
set /p op=">>> Selecciona una opcion [1-4]: "

if "%op%"=="1" goto subir
if "%op%"=="2" goto estado
if "%op%"=="3" goto historial
if "%op%"=="4" exit

:subir
cls
echo ========================================
echo    SUBIENDO CAMBIOS A GITHUB
echo ========================================
echo.

:: 1. Verificar si hay .git
if not exist .git (
    echo [1/6] Inicializando repositorio...
    git init
) else (
    echo [1/6] Repositorio inicializado correctamente.
)

:: 2. Limpiar basura temporal
echo [2/6] Limpiando archivos temporales (ZIPs, logs, backups)...
del *.zip 2>nul
del *.log 2>nul
for /d %%i in (backup_*) do rmdir /s /q "%%i" 2>nul
rmdir /s /q tmp 2>nul
rmdir /s /q __pycache__ 2>nul

:: 3. Crear .gitignore si no existe
echo [3/6] Verificando .gitignore...
if not exist .gitignore (
    echo *.zip > .gitignore
    echo *.7z >> .gitignore
    echo *.rar >> .gitignore
    echo *.log >> .gitignore
    echo backup_*/ >> .gitignore
    echo tmp/ >> .gitignore
    echo __pycache__/ >> .gitignore
    echo .ipynb_checkpoints/ >> .gitignore
    echo .vscode/ >> .gitignore
    echo [OK] .gitignore creado.
) else (
    echo [OK] .gitignore ya existe.
)

:: 4. Añadir archivos
echo [4/6] Añadiendo archivos...
git add .

:: 5. Commit
echo [5/6] Confirmando commit...
set fecha=%date:~10,4%-%date:~4,2%-%date:~7,2% %time:~0,2%:%time:~3,2%
git commit -m "Actualizacion EINSTEIN-VED - %fecha%"

:: 6. Push (detectar rama y forzar si es necesario)
echo [6/6] Subiendo a GitHub...
for /f %%i in ('git branch --show-current 2^>nul') do set rama=%%i
if "%rama%"=="" set rama=main

:: Añadir remoto si no existe
git remote add origin https://github.com/quark-cha/Einstein-VED.git 2>nul

:: Subir con force para resolver conflictos
git push -u origin %rama% --force

echo.
echo ========================================
echo [OK] Repositorio actualizado
echo https://github.com/quark-cha/Einstein-VED
echo ========================================
pause
goto menu

:estado
cls
echo ========================================
echo    ESTADO DEL REPOSITORIO
echo ========================================
echo.
git status
echo.
pause
goto menu

:historial
cls
echo ========================================
echo    HISTORIAL DE COMMITS
echo ========================================
echo.
git log --oneline --decorate --graph -10
echo.
pause
goto menu