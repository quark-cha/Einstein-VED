@echo off
title FORZAR GITHUB A ESTADO CORRECTO
color 0C

echo ============================================
echo    EMERGENCIA: REPARAR GITHUB
echo ============================================
echo ⚠️  ESTADO ACTUAL INCORRECTO:
echo    • GitHub TIENE img/ (NO debería)
echo    • GitHub NO TIENE proyecto/ (SI debería)
echo    • GitHub NO TIENE .gitignore (SI debería)
echo.
echo 🎯 ESTO HARÁ:
echo    1. Crear .gitignore correcto
echo    2. Forzar proyecto/ a GitHub
echo    3. Eliminar img/ de GitHub
echo    4. GitHub = Copia exacta de TU PC
echo.

set /p confirm="¿FORZAR GitHub a estado CORRECTO? (ESCRIBE 'FORZAR'): "
if not "%confirm%"=="FORZAR" (
    echo Cancelado.
    pause
    exit /b
)

echo.
echo ======= 1. CREANDO .gitignore CORRECTO =======
(
echo # EXCLUSIONES EINSTEIN-VED
echo # ========================
echo.
echo # IMAGENES (se generan localmente)
echo img/
echo *.png
echo *.svg
echo *.jpg
echo *.jpeg
echo *.gif
echo.
echo # TEMPORALES
echo __pycache__/
echo *.pyc
echo *.log
echo *.tmp
echo *.bak
echo *~
echo.
echo # CONFIGURACIONES LOCALES
echo .env
echo .venv/
echo .vscode/
) > .gitignore
echo ✅ .gitignore creado

echo.
echo ======= 2. AÑADIENDO ARCHIVOS CORRECTOS =======
git add .gitignore
git add proyecto/
git add src/
git add tools/
git add dic/
git add *.md 2>nul
echo ✅ Archivos correctos añadidos

echo.
echo ======= 3. ELIMINANDO img/ DE GIT =======
git rm -r --cached img/ 2>nul
echo ✅ img/ marcada para eliminación

echo.
echo ======= 4. COMMIT DEFINITIVO =======
git commit -m "EMERGENCY FIX: Estado correcto - Con proyecto/, sin img/, con .gitignore"
echo ✅ Commit creado

echo.
echo ======= 5. FORZANDO GITHUB =======
echo 🚀 ENVIANDO estado CORRECTO a GitHub...
git push origin master --force
echo.

echo ============================================
echo    ✅ GITHUB REPARADO
echo ============================================
echo.
echo 📊 AHORA GITHUB TIENE:
echo    ✅ proyecto/ (con GIT.bat)
echo    ✅ .gitignore (excluye img/)
echo    ✅ src/, tools/, dic/
echo    ❌ img/ (ELIMINADA de GitHub)
echo.
echo 🌐 VERIFICA: https://github.com/quark-cha/Einstein-VED
echo.
echo ⚠️  Las imágenes siguen en TU PC: %CD%\img\
echo.
pause