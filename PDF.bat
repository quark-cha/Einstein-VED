@echo off
setlocal enabledelayedexpansion

:: =============================
:: MENÚ DE SELECCIÓN
:: =============================
echo.
echo ===============================================
echo ¿QUÉ QUIERES SUBIR AL SERVIDOR FTP?
echo -----------------------------------------------
echo 1 - Solo PDFs
echo 2 - Solo Markdown (.md)
echo 3 - Solo imágenes (png/svg)
echo 4 - TODO
echo ===============================================
echo.
set /p "OPTION=Elige una opción (1-4): "

set "SEND_PDF=0"
set "SEND_MD=0"
set "SEND_IMG=0"

if "%OPTION%"=="1" set "SEND_PDF=1"
if "%OPTION%"=="2" set "SEND_MD=1"
if "%OPTION%"=="3" set "SEND_IMG=1"
if "%OPTION%"=="4" (
    set "SEND_PDF=1"
    set "SEND_MD=1"
    set "SEND_IMG=1"
)

:: =============================
:: CONFIGURACIÓN
:: =============================
set "SRC_DIR=C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED"
set "FTP_SERVER=estradad.es"
set "FTP_USER=estradad.es"
set "FTP_PASS=%FTP_PASS_PDF%"
set "LOG_FILE=%SRC_DIR%\PDF-FTP.log"
set "FTP_SCRIPT=%TEMP%\ftp_script.txt"

set "FTP_REMOTE_PDF=teorias/pdf/Einstein-VED"
set "FTP_REMOTE_MD=teorias/pdf/Einstein-VED/md"
set "FTP_REMOTE_IMG=teorias/pdf/Einstein-VED/img"

del "%FTP_SCRIPT%" 2>nul
del "%LOG_FILE%" 2>nul

:: =============================
:: CREAR LISTAS DE ARCHIVOS PRIMERO
:: =============================
set "PDF_LIST="
set "MD_LIST="
set "PNG_LIST="
set "SVG_LIST="

:: Buscar archivos PDF
if "%SEND_PDF%"=="1" (
    echo Buscando PDFs...
    for %%F in ("%SRC_DIR%\*.pdf") do (
        set "PDF_LIST=!PDF_LIST! "%%F""
    )
)

:: Buscar archivos Markdown
if "%SEND_MD%"=="1" (
    echo Buscando archivos .md...
    for %%F in ("%SRC_DIR%\*.md") do (
        set "MD_LIST=!MD_LIST! "%%F""
    )
)

:: Buscar imágenes PNG
if "%SEND_IMG%"=="1" (
    echo Buscando imágenes PNG...
    for %%F in ("%SRC_DIR%\*.png") do (
        set "PNG_LIST=!PNG_LIST! "%%F""
    )
    echo Buscando imágenes SVG...
    for %%F in ("%SRC_DIR%\*.svg") do (
        set "SVG_LIST=!SVG_LIST! "%%F""
    )
)

:: =============================
:: CREAR SCRIPT FTP
:: =============================
echo Creando script FTP...

(
    echo open %FTP_SERVER%
    echo user %FTP_USER% %FTP_PASS%
    echo binary
    echo prompt off

    :: Subir PDFs
    if "%SEND_PDF%"=="1" (
        echo ! Subiendo PDFs...
        echo cd %FTP_REMOTE_PDF%
        for %%F in (%PDF_LIST%) do (
            echo put %%F
        )
    )

    :: Subir Markdown
    if "%SEND_MD%"=="1" (
        echo ! Subiendo Markdown...
        echo cd %FTP_REMOTE_MD%
        for %%F in (%MD_LIST%) do (
            echo put %%F
        )
    )

    :: Subir imágenes
    if "%SEND_IMG%"=="1" (
        echo ! Subiendo imágenes...
        echo cd %FTP_REMOTE_IMG%
        for %%F in (%PNG_LIST%) do (
            echo put %%F
        )
        for %%F in (%SVG_LIST%) do (
            echo put %%F
        )
    )

    echo bye
) > "%FTP_SCRIPT%"

echo Script FTP creado en: %FTP_SCRIPT%

:: =============================
:: EJECUTAR FTP
:: =============================
echo.
echo ========================================
echo EJECUTANDO TRANSFERENCIA FTP...
echo ========================================
echo.

ftp -n -s:"%FTP_SCRIPT%" > "%LOG_FILE%" 2>&1

:: Verificar resultados
echo.
echo ========================================
echo RESUMEN DE TRANSFERENCIA
echo ========================================
if "%SEND_PDF%"=="1" (
    echo PDFs encontrados: %PDF_LIST: =&echo.%
    echo.
)
if "%SEND_MD%"=="1" (
    echo MD encontrados: %MD_LIST: =&echo.%
    echo.
)
if "%SEND_IMG%"=="1" (
    echo PNG encontrados: %PNG_LIST: =&echo.%
    echo SVG encontrados: %SVG_LIST: =&echo.%
    echo.
)

echo.
echo ========================================
echo PROCESO COMPLETADO
echo ----------------------------------------
echo Revisa el log en:
echo   %LOG_FILE%
echo ========================================

:: Agregar marca de tiempo al log
echo %date% %time% - FIN FTP >> "%LOG_FILE%"

:: Mostrar últimas líneas del log
echo.
echo Últimas líneas del log:
echo ------------------------
type "%LOG_FILE%" | tail -5 2>nul
if errorlevel 1 (
    echo Mostrando todo el log:
    echo ------------------------
    type "%LOG_FILE%"
)

pause