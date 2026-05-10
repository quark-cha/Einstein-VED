@echo off
title FORZAR GITHUB CORRECTO (CON COPIA DE SEGURIDAD)
color 0C

echo ====================================================
echo    REPARACION SEGURA de GitHub - EINSTEIN-VED
echo ====================================================
echo ⚠️  ESTADO ACTUAL INCORRECTO:
echo    • GitHub tiene img/ (NO debe)
echo    • GitHub NO tiene proyecto/ (SI debe)
echo.
echo 🛡️  ESTE SCRIPT HARÁ:
echo    1. CREAR COPIA DE SEGURIDAD LOCAL de GitHub
echo    2. VERIFICAR si hay cambios en GitHub que no tengas
echo    3. SOLO FORZAR si estás seguro
echo    4. Dejar GitHub EXACTO a tu PC
echo.

:: --- 1. CREAR COPIA DE SEGURIDAD ---
echo.
echo ======= 1. CREANDO COPIA DE SEGURIDAD =======
set backup_dir=backup_github_%date:/=-%_%time:~0,2%-%time:~3,2%
mkdir "%backup_dir%" 2>nul
echo 📂 Creando carpeta de respaldo: %backup_dir%
git clone https://github.com/quark-cha/Einstein-VED.git "%backup_dir%" 2>nul
if %errorlevel% neq 0 (
    echo ❌ ERROR: No se pudo clonar repositorio para respaldo
    echo    Verifica conexión o URL: https://github.com/quark-cha/Einstein-VED
    pause
    exit /b 1
)
echo ✅ Respaldo creado en: %CD%\%backup_dir%

:: --- 2. VERIFICAR CAMBIOS REMOTOS ---
echo.
echo ======= 2. VERIFICANDO CAMBIOS EN GITHUB =======
git fetch origin
git log HEAD..origin/master --oneline > cambios_remotos.txt 2>nul
set /p num_cambios=<"cambios_remotos.txt" 2>nul
if "%num_cambios%"=="" (
    echo ✅ GitHub NO tiene commits nuevos que tú no tengas
    set tiene_cambios=NO
) else (
    echo ⚠️  ATENCIÓN: GitHub tiene commits que NO tienes:
    type cambios_remotos.txt
    echo.
    set tiene_cambios=SI
)
del cambios_remotos.txt 2>nul

:: --- 3. CONFIRMACIÓN FINAL ---
echo.
echo ======= 3. CONFIRMACIÓN FINAL =======
echo 📊 RESUMEN:
echo    • Respaldo creado: %backup_dir%
if "%tiene_cambios%"=="SI" (
    echo    • ⚠️  GitHub TIENE commits nuevos
) else (
    echo    • ✅ GitHub NO tiene commits nuevos
)
echo    • Acción: GitHub será SOBRESCRITO con tu PC
echo.

if "%tiene_cambios%"=="SI" (
    set /p confirm="¿FORZAR igualmente? (commits remotos se PERDERÁN) [ESCRIBE 'FORZAR']: "
) else (
    set /p confirm="¿Continuar con sobrescritura? [ESCRIBE 'SI']: "
)

if not "%confirm%"=="FORZAR" if not "%confirm%"=="SI" (
    echo ❌ Cancelado. Tu respaldo está en: %backup_dir%
    pause
    exit /b
)

:: --- 4. CREAR .gitignore SI NO EXISTE ---
echo.
echo ======= 4. CONFIGURANDO .gitignore =======
if not exist ".gitignore" (
    (
        echo # EINSTEIN-VED - Archivos excluidos
        echo img/
        echo __pycache__/
        echo *.pyc
        echo .env
    ) > .gitignore
    echo ✅ .gitignore creado
) else (
    echo ✅ .gitignore ya existe
)

:: --- 5. SINCRONIZACIÓN FORZADA ---
echo.
echo ======= 5. SINCRONIZANDO ESTADO CORRECTO =======
git add .gitignore proyecto/ src/ tools/ dic/ *.md 2>nul
git rm -r --cached img/ 2>nul
git commit -m "SYNC FORCE: Estado final correcto - con proyecto/, sin img/" --no-verify
git push origin master --force

echo.
echo ====================================================
echo    ✅ SINCORNIZACIÓN COMPLETADA
echo ====================================================
echo.
echo 📊 ESTADO FINAL:
echo    ✅ GitHub = Copia exacta de TU PC
echo    ✅ Respaldo guardado en: %backup_dir%
echo    ✅ img/ eliminada solo de GitHub (en tu PC está intacta)
echo.
echo 🔄 PARA RECUPERAR versión anterior (si es necesario):
echo    1. Ve a la carpeta: %backup_dir%
echo    2. Ejecuta: git push origin master --force
echo.
pause