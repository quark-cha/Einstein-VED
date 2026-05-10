@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ============================================
:: CONFIGURACIÓN
:: ============================================
set "DIC_DIR=%~dp0..\dic"
set "MODO_SIM=1"

:: Parámetros
if "%~1"=="--limpiar" set "MODO_SIM=0"
if "%~1"=="-l" set "MODO_SIM=0"
if "%~1"=="--simular" set "MODO_SIM=1"
if "%~1"=="-s" set "MODO_SIM=1"
if "%~1"=="--help" goto :ayuda

:: ============================================
:: FUNCIÓN PRINCIPAL
:: ============================================
echo.
echo ========================================================
echo 🧹 LIMPIADOR DE LÍNEAS SIN CORRESPONDENCIA EN ESPAÑOL
echo ========================================================
echo 📂 Directorio: %DIC_DIR%
echo.

if not exist "%DIC_DIR%" (
    echo ❌ Error: No existe %DIC_DIR%
    pause
    exit /b 1
)

set total_procesados=0
set lineas_eliminadas=0
set archivos_modificados=0

:: Para cada archivo que NO sea español
for %%F in ("%DIC_DIR%\??-*.dic") do (
    set "archivo_actual=%%F"
    set "nombre_archivo=%%~nxF"
    set "prefijo=!nombre_archivo:~0,2!"
    
    :: Solo procesar archivos que NO empiezan con "es"
    if /i not "!prefijo!"=="es" (
        
        :: Extraer nombre base COMPLETO (incluyendo .py si existe)
        set "nombre_base=!nombre_archivo:~3!"
        set "nombre_base=!nombre_base:~0,-4!"
        
        :: Construir nombre del diccionario español correspondiente
        set "archivo_espanol=%DIC_DIR%\es-!nombre_base!.dic"
        
        :: Verificar si existe el diccionario español
        if exist "!archivo_espanol!" (
            set /a total_procesados+=1
            
            echo.
            echo 🔍 Procesando: !nombre_archivo!
            echo   Español: es-!nombre_base!.dic
            
            :: Leer diccionario español y crear índice de campos 2,3 en ARCHIVO TEMPORAL
            set "temp_indice=%TEMP%\indice_!random!.tmp"
            (
                for /f "usebackq tokens=1,2,3 delims=;" %%a in ("!archivo_espanol!") do (
                    echo %%b;%%c
                )
            ) > "!temp_indice!"
            
            :: Contar líneas en español
            set "lineas_es=0"
            for /f %%i in ('type "!archivo_espanol!" ^| find /c /v ""') do set "lineas_es=%%i"
            
            :: Procesar diccionario actual
            set "temp_limpio=%TEMP%\limpio_!random!.tmp"
            set "lineas_totales=0"
            set "lineas_mantenidas=0"
            set "lineas_borradas=0"
            
            (
                for /f "usebackq tokens=1,2,3* delims=;" %%a in ("!archivo_actual!") do (
                    set /a lineas_totales+=1
                    
                    :: Construir clave: campo2;campo3
                    set "clave_actual=%%b;%%c"
                    
                    :: Verificar si la clave existe en el índice español (usando find)
                    findstr /b /c:"!clave_actual!" "!temp_indice!" >nul
                    
                    :: Si existe, mantener la línea
                    if not errorlevel 1 (
                        set /a lineas_mantenidas+=1
                        echo %%a;%%b;%%c;%%d
                    ) else (
                        set /a lineas_borradas+=1
                        set /a lineas_eliminadas+=1
                        if "!MODO_SIM!"=="1" (
                            echo   🟡 Eliminaría: %%a;%%b;%%c...
                        )
                    )
                )
            ) > "!temp_limpio!"
            
            :: Mostrar estadísticas REALES
            echo   Líneas en español: !lineas_es!
            echo   Líneas en !prefijo!: !lineas_totales!
            echo   Líneas mantendría: !lineas_mantenidas!
            echo   Líneas eliminaría: !lineas_borradas!
            
            :: Si hay líneas para eliminar y no es simulación, reemplazar archivo
            if !lineas_borradas! gtr 0 (
                if "!MODO_SIM!"=="0" (
                    :: Crear copia de seguridad
                    copy "!archivo_actual!" "!archivo_actual!.bak" >nul
                    
                    :: Reemplazar archivo original
                    move /y "!temp_limpio!" "!archivo_actual!" >nul
                    
                    if errorlevel 1 (
                        echo   ❌ Error al actualizar archivo
                    ) else (
                        echo   ✅ Archivo actualizado
                        set /a archivos_modificados+=1
                    )
                )
            ) else (
                :: Limpiar temporal si no hay cambios
                del "!temp_limpio!" 2>nul
            )
            
            :: Limpiar archivo temporal de índice
            del "!temp_indice!" 2>nul
            
        ) else (
            echo.
            echo ⚠️  !nombre_archivo! - No tiene es-!nombre_base!.dic
            echo   (Se ignorará - no tiene diccionario español de referencia)
        )
    )
)

:: ============================================
:: RESUMEN
:: ============================================
echo.
echo ========================================================
echo 📊 RESUMEN FINAL
echo ========================================================
echo Archivos procesados: %total_procesados%
echo Líneas eliminadas: %lineas_eliminadas%
echo Archivos modificados: %archivos_modificados%
echo.

if "%MODO_SIM%"=="1" (
    echo 🔍 MODO SIMULACIÓN
    echo    Solo se mostró qué líneas se eliminarían
    echo.
    echo ⚠️  Para eliminar realmente, ejecuta:
    echo    %~nx0 --limpiar
    echo    %~nx0 -l
) else (
    echo ✅ Proceso completado
    echo   Se crearon copias .bak de los archivos modificados
)

echo.
pause
exit /b 0

:ayuda
echo.
echo ========================================================
echo 📖 AYUDA: %~nx0
echo ========================================================
echo.
echo USO: %~nx0 [OPCIÓN]
echo.
echo Este script compara cada diccionario XX-nombre.dic con su
echo correspondiente es-nombre.dic y elimina las líneas que NO
echo tienen correspondencia en los CAMPOS 2 Y 3.
echo.
echo FORMATO DE LÍNEA: campo1;campo2;campo3;campo4...
echo COMPARACIÓN: Se comparan campo2;campo3
echo.
echo OPCIONES:
echo   Sin opciones          Modo simulación (solo muestra)
echo   -s, --simular         Modo simulación (solo muestra)
echo   -l, --limpiar         Modo limpieza real (elimina líneas)
echo   --help                Muestra esta ayuda
echo.
echo EJEMPLOS:
echo   %~nx0                 Muestra qué líneas se eliminarían
echo   %~nx0 --limpiar       Elimina realmente las líneas
echo.
echo NOTA: Se crean copias .bak de los archivos modificados.
pause
exit /b 0