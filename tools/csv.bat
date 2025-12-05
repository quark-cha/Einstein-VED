@echo off
set "salida=..\tmp\global.csv"

:: Crear carpeta tmp si no existe
if not exist "..\tmp" mkdir ..\tmp

:: Borrar archivo de salida si existe
if exist "%salida%" del "%salida%"

:: Recorrer todos los CSV en dic y subcarpetas
for /R "..\dic" %%f in (*.csv) do (
    echo Procesando %%f
    type "%%f" >> "%salida%"
)

echo ✅ Todos los CSV combinados en %salida%
pause


