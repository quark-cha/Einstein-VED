# Guía de Normas para Scripts del Proyecto

**Normas a seguir en este proyecto**  

> Todo esto se hará como comentario en los scripts  

## 1. Encabezado de archivo

- Primera línea: nombre del fichero.  
- Segunda línea: vacía.  
- Tercera línea en adelante: descripción de lo que hace el script.  
- Línea recta:  

# 0-busca-regenera.py
#
# Este módulo procesa archivos .py y sus diccionarios de traducción.
#
# Funcionalidad:
#   - Busca el diccionario español correspondiente al archivo.py.
#   - Recopila todas las líneas de traducciones en otros idiomas.
#   - Solo incorpora líneas válidas si coinciden con el diccionario español.
#   - Omite líneas repetidas o incompletas.
#   - Renombra los CSV procesados para evitar reprocesarlos.
#   - Soporta procesar un archivo específico o todos los archivos con el argumento "todas"/"todo".
#
# Entradas:
#   - archivo.py (o campo2.py) a procesar.
#   - CSV de traducciones en directorio tmp.
#   - Diccionario español correspondiente (es_<campo>.dic).
#
# Salidas:
#   - Diccionarios de cada idioma actualizados (fr_<campo>.dic, de_<campo>.dic, etc.).
#   - Archivos CSV renombrados como <archivo>.csv_procesado.
#   - Logs en ..\log\<proceso-principal>.log.
#
# Argumentos:
#   - nombre del archivo.py o "todas"/"todo".
#
# ===================================================
# Autor: Victor Estrada Díaz
# Licencia: CC BY-SA y Licencia Ética
# URL Licencia Ética: https://estradad.es/licencia.php
