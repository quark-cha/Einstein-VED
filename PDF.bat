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

:: =============================
:: CREAR SCRIPT FTP
:: =============================
(
    echo open %FTP_SERVER%
    echo user %FTP_USER% %FTP_PASS%
    echo binary
    echo prompt off

    :: PDFs
    if "%SEND_PDF%"=="1" (
        echo cd %FTP_REMOTE_PDF%
        for %%F in (%SRC_DIR%\*.pdf) do echo put %%F
    )

    :: Markdown
    if "%SEND_MD%"=="1" (
        echo cd %FTP_REMOTE_MD%
        for %%F in (%SRC_DIR%\*.md) do echo put %%F
    )

    :: Imágenes
    if "%SEND_IMG%"=="1" (
        echo cd %FTP_REMOTE_IMG%
        for %%F in (%SRC_DIR%\*.png) do echo put %%F
        for %%F in (%SRC_DIR%\*.svg) do echo put %%F
    )

    echo bye
) > "%FTP_SCRIPT%"

:: =============================
:: EJECUTAR FTP
:: =============================
ftp -n -s:"%FTP_SCRIPT%" > "%LOG_FILE%" 2>&1
echo %date% %time% - FIN FTP >> "%LOG_FILE%"

echo.
echo ========================================
echo     PROCESO COMPLETADO
echo ----------------------------------------
echo Revisa:
echo   %LOG_FILE%
echo ========================================
pause
