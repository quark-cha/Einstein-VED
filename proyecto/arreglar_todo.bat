@echo off
title ARREGLAR TODO - Einstein-VED
color 0C

echo ====================================
echo    ARREGLAR SITUACIÓN GIT
echo ====================================
echo 📊 PROBLEMAS DETECTADOS:
echo 1. master divergido (5 commits diferencia)
echo 2. img/ no debería estar en git
echo 3. proyecto/ no está en git
echo 4. .gitignore no está en git
echo.

echo ⚠️  Esto hará:
echo    • Sincronizar master con GitHub
echo    • Añadir proyecto/ y .gitignore
echo    • Excluir img/ permanentemente
echo.

set /p confirm="¿Continuar? (s/n): "
if /i "%confirm%" neq "s" exit /b

echo.
echo ====================================
echo    1. SINCRONIZANDO MASTER
echo ====================================
git stash
git pull origin master --rebase
git stash pop

echo.
echo ====================================
echo    2. ORGANIZANDO ARCHIVOS
echo ====================================
git add .gitignore
git add proyecto/
git add tools/
git rm --cached -r img/ 2>nul
(
echo # ====================================
echo # EXCLUSIONES Einstein-VED
echo # ====================================
echo.
echo # IMÁGENES (se generan con scripts)
echo img/
echo *.png
echo *.svg
echo *.jpg
echo *.jpeg
echo.
echo # TEMPORALES
echo __pycache__/
echo *.pyc
echo *.log
echo *.tmp
echo *.bak
) > .gitignore

echo.
echo ====================================
echo    3. CREANDO COMMIT
echo ====================================
git add .
git commit -m "FIX: Organización proyecto + exclusión imágenes"

echo.
echo ====================================
echo    4. SUBIENDO A GITHUB
echo ====================================
git push origin master

echo.
echo ====================================
echo    ✅ COMPLETADO
echo ====================================
echo.
echo 📊 ESTADO FINAL:
git status
echo.
echo 🌐 GitHub: https://github.com/quark-cha/Einstein-VED
echo.
pause