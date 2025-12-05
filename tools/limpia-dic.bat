@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Configuración
set "DIC_DIR=%~dp0..\dic"
set "MODO_SIM=0"

:: Parámetros
if "%~1"=="--simular" set "MODO_SIM=1"
if "%~1"=="-s" set "MODO_SIM=1"
if "%~1"=="--help" goto :ayuda

echo 🗑️  Limpiando diccionarios sin referencia española...
echo 📂 Directorio: %DIC_DIR%
echo.

if not exist "%DIC_DIR%" (
    echo ❌ Error: No existe %DIC_DIR%
    pause
    exit /b 1
)

set cnt=0
set del=0

:: Primero, obtener lista de diccionarios españoles
echo 🔍 Buscando diccionarios españoles...
for %%f in ("%DIC_DIR%\es-*.dic") do (
    set "es_file=%%~nxf"
    :: Extraer nombre base (es-script.dic -> script)
    set "base_name=!es_file:~3,-4!"
    echo   ✅ Encontrado: !es_file! (base: !base_name!)
)

echo.

:: Ahora procesar otros idiomas
for %%f in ("%DIC_DIR%\??-*.dic") do (
    set "file=%%~nxf"
    set "pref=!file:~0,2!"
    
    if /i not "!pref!"=="es" (
        set /a cnt+=1
        
        :: Extraer nombre base correctamente
        set "base_name=!file:~3!"
        
        :: CORRECCIÓN: Buscar diccionario español correspondiente
        :: Si tenemos en-script1.py.dic, necesitamos es-script1.dic
        :: Pero primero intentamos coincidencia exacta
        
        :: Quitar extensión .dic
        set "search_base=!base_name:~0,-4!"
        
        :: Quitar .py si existe (para archivos .py.dic)
        if "!search_base:~-3!"==".py" (
            set "search_base=!search_base:~0,-3!"
        )
        
        :: Nombre del diccionario español a buscar
        set "es_to_find=es-!search_base!.dic"
        
        echo 🔍 Verificando !file!...
        echo   Buscando: !es_to_find!
        
        if not exist "%DIC_DIR%\!es_to_find!" (
            echo ❌ !file! (sin !es_to_find!)
            if "!MODO_SIM!"=="0" (
                del "%%f" && (
                    echo   ✅ Eliminado
                    set /a del+=1
                ) || echo   ❌ Error al eliminar
            ) else (
                echo   🔍 Se eliminaría
                set /a del+=1
            )
        ) else (
            echo   ✅ Tiene referencia: !es_to_find!
        )
        echo.
    )
)

echo.
echo 📊 Resumen:
echo   Analizados: %cnt%
echo   Sin referencia: %del%
echo.

if "%MODO_SIM%"=="1" (
    echo 🔍 Modo simulación - No se eliminaron archivos
) else (
    if %del% equ 0 (
        echo ✅ Todos tienen referencia española
    ) else (
        echo ⚠️  Eliminados: %del% archivos
    )
)

pause
exit /b 0

:ayuda
echo Uso: %~nx0 [-s | --simular | --help]
echo.
echo Elimina diccionarios ff-*.dic sin es-*.dic correspondiente.
echo Busca en ..\dic por defecto.
echo.
echo   -s, --simular  Solo muestra qué se eliminaría
echo   --help        Muestra esta ayuda
pause