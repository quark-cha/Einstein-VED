import os
import re
import runpy
from pathlib import Path
import csv

# ==============================
# DIRECTORIOS DEL PROYECTO
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR  = BASE_DIR / "src"
DIC_DIR  = BASE_DIR / "dic"
IMG_DIR  = BASE_DIR / "img"
TMP_DIR  = BASE_DIR / "tmp"

IMG_DIR.mkdir(exist_ok=True)
TMP_DIR.mkdir(exist_ok=True)

#print(f"📂 Directorio base: {BASE_DIR}")
#print(f"📂 SRC listo: {SRC_DIR}")
#print(f"📂 TMP listo: {TMP_DIR}")
#print(f"📂 IMG listo: {IMG_DIR}")
#print(f"📂 Diccionarios: {DIC_DIR}")

# ==============================
# PREFIJOS POR IDIOMA
# ==============================

PREFIJOS = {
    "es": "ES_",
    "en": "EN_",
    "fr": "FR_",
    "it": "IT_",
    "de": "DE_",
    "ar": "AR_",
    "ja": "JA_",
    "zh": "ZH_",
    "pt": "PT_",
    "sk": "SK_",
    "ast": "AST_",
    "el": "EL_"
}

def obtener_prefijo(idioma):
    return PREFIJOS.get(idioma, "")

NO_TRADUCIR = [
    # Backends
    "agg", "tkagg", "qt5agg", "qt4agg", "wxagg", "macosx", "pdf", "ps", "svg",

    # Fonts
    "normal", "italic", "oblique",
    "sans-serif", "serif", "monospace", "cursive", "fantasy",
    "light", "medium", "semibold", "bold", "heavy", "black",
    "condensed", "expanded",
    "dejavusans", "dejavuserif", "dejavusansmono",

    # Layout & alignment
    "tight", "tight_layout", "center", "baseline",
    "left", "right", "top", "bottom", "center_baseline", "center_y",
    "auto", "best", "off", "on",
    "upper right", "upper left", "lower right", "lower left",
    "center right", "center left",

    # Lines and markers
    "solid", "dashed", "dashdot", "dotted",
    "o", "s", "^", "v", "<", ">", "*", "+", "x", ".", ",",
    "markersize", "markeredgewidth", "markerfacecolor", "markeredgecolor",

    # Axes scales and ticks
    "linear", "log", "symlog", "logit",
    "major", "minor", "both",

    # Plots & axes types
    "polar", "rectilinear",
    "figure", "axes", "subplot", "gridspec", "legend", "colorbar",

    # Figure properties
    "linewidth", "fontsize", "fontweight", "fontstyle",
    "alpha", "zorder", "bbox_inches",
    "dpi", "format", "facecolor", "edgecolor",

    # Boolean values
    "true", "false", "none",

    # Box styles (FancyBboxPatch)
    "round", "round4", "roundtooth", "roundpad", "square",
    "larrow", "rarrow", "darrow", "ltriangle", "rtriangle", "angle",
    "mutation_scale", "mutation_aspect", "pad", "rounding_size", "boxstyle",
    "round,pad=0.8", "round,pad=0.5", "round,pad=0.3",  "round,pad=0.6",

    # Mathtext
    "rm", "it", "bf", "sf", "tt",

    # Valores numéricos como strings para evitar traducción accidental
    "0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1.0","6","8","10",

    # Misc / internal
    "__main__", "__init__"
]




# ==============================
# IDIOMAS DISPONIBLES PARA UN PY
# ==============================

def obtener_idiomas_para_py(nombre_archivo_py):
    """
    Devuelve la lista de idiomas que tienen diccionario
    para un fichero .py concreto.
    """
    patron = f"*-{nombre_archivo_py.stem}.dic"
    idiomas = []

    for dic in DIC_DIR.glob(patron):
        idioma = dic.name.split("-")[0]
        if idioma != "es":  # español nunca es destino
            idiomas.append(idioma)

    return sorted(set(idiomas))

# ==============================
# CARGAR DICCIONARIOS
# ==============================

def cargar_diccionario(archivo):
    dic_file = DIC_DIR / archivo
    if not dic_file.exists():
        print(f"[AVISO] No existe {dic_file}")
        return {}

    pares = {}
    with dic_file.open("r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)  # saltar cabecera
        for fila in reader:
            if len(fila) < 4:
                continue
            id_linea = fila[2].strip()
            texto = fila[3]
            pares[id_linea] = texto

    return pares

# ==============================
# APLICAR DICCIONARIO
# ==============================

def limpiar_escapes(s):
    return (
        s.replace("\\n", "\n")
         .replace("\\t", "\t")
         .replace("\\r", "\r")
         .replace("\\\"", "\"")
         .replace("\\'", "'")
         .replace("\\\\", "\\")
    )

import unicodedata

def contiene_letras_latinas(texto, min_letras=3):
    """
    Devuelve True si el texto contiene al menos `min_letras` caracteres latinos.
    Ignora números, símbolos, fórmulas y caracteres no latinos.
    """
    contador = 0
    for c in texto:
        if c.isalpha():
            try:
                nombre = unicodedata.name(c)
            except ValueError:
                continue
            if "LATIN" in nombre:
                contador += 1
                if contador >= min_letras:
                    return True
    return False


def extraer_cadenas_traducibles(contenido):
    """
    Devuelve cadenas literales traducibles en el código.
    Ignora:
    - Claves de diccionarios y rcParams
    - Valores de parámetros de librerías
    """
    cadenas = re.findall(r'(["\'])(.+?)\1', contenido)
    traducibles = []

    for _, texto in cadenas:
        # Ignorar si la cadena está dentro de corchetes (clave de diccionario)
        if re.search(r'\[\s*["\']' + re.escape(texto) + r'["\']\s*\]', contenido):
            continue

        # Ignorar si parece un valor de parámetro (contiene = o combinaciones con números)
        if re.search(r'^\s*\w+\s*=', texto) or re.search(r'[=,]\s*\d', texto):
            continue

        # Ignorar si no tiene al menos 3 letras latinas
        if not contiene_letras_latinas(texto, min_letras=3):
            continue

        traducibles.append(texto)

    return traducibles


def aplicar_diccionario(contenido, dic_es, dic_dest):
    """
    Reemplaza en el contenido las cadenas traducibles según diccionarios.
    """
    # Extraer cadenas traducibles
    cadenas = extraer_cadenas_traducibles(contenido)
    
    # Convertimos las claves a lista ordenada para recorrerlas por índice
    claves_es = list(dic_es.keys())  # ['25', '58', ...]
    claves_dest = list(dic_dest.keys())  # ['25', '58', ...]
    for i in range(len(claves_es)):
        if claves_es[i] != claves_dest[i]:
            print(f"⚠️ Las lineas no coinciden en los diccionarios: {claves_es[i]} != {claves_dest[i]}")
            print("❌ Abortando traducción.Erroneas en los diccionarios.")
            return contenido
        texto_es = dic_es.pop(claves_es[i])
        texto_dest = dic_dest.pop(claves_dest[i])  # asumiendo que dic_dest tiene las mismas claves
        
        # --- CASO 1: no hay salto de línea ---
        if "\\n" not in texto_es:
            if texto_es not in NO_TRADUCIR:
                contenido = contenido.replace(texto_es, texto_dest)
            continue

        # --- CASO 2: hay salto de línea ---
        partes_es = texto_es.split("\\n")
        partes_dest = texto_dest.split("\\n")

        # Comprobación de consistencia
        if len(partes_es) != len(partes_dest):
            print(
                f"⚠️ Diccionarios NO coinciden {partes_es}!={partes_dest}: "
                f"{len(partes_es)} vs {len(partes_dest)} trozos"
            )
            continue

        # Reemplazo trozo a trozo
        for p_es, p_dest in zip(partes_es, partes_dest):
            if p_es not in NO_TRADUCIR:
                contenido = contenido.replace(p_es, p_dest)
                

        if texto_es not in NO_TRADUCIR:
            contenido = contenido.replace(texto_es, texto_dest)  
    
    return contenido


# ==============================
# CORREGIR SAVE / SAVEFIG
# ==============================

def corregir_save(contenido, idioma):
    import os, re

    if idioma not in PREFIJOS:
        print(f"❌ Idioma desconocido para prefijo: {idioma}")
        return contenido

    dir_img = IMG_DIR.resolve()
    prefijo = obtener_prefijo(idioma)

    patron = r'(save|savefig)\(\s*([\'"])([^\'"]+)\2'

    def reemplazo(m):
        ruta_original = m.group(3)
        nombre = os.path.basename(ruta_original)

        # Evitar doble prefijo
        if nombre.startswith(prefijo):
            return m.group(0)

        nombre_sin_ext, ext = os.path.splitext(nombre)
        nuevo_nombre = f"{prefijo}{nombre_sin_ext}{ext}"
        nueva_ruta = dir_img / nuevo_nombre

        # 🔑 Escape para código Python
        ruta_txt = str(nueva_ruta).replace("\\", "\\\\")

        return m.group(0).replace(ruta_original, ruta_txt)

    return re.sub(patron, reemplazo, contenido)
    
    
# ==============================
# PROCESAR UN ARCHIVO PY
# ==============================

def procesar_py(nombre_archivo_py, idioma):
    """
    Procesa un archivo .py, traduciendo usando diccionarios y guardando
    un temporal en TMP_DIR con prefijo <IDIOMA>_. Luego ejecuta
    el temporal directamente en el mismo proceso.
    """

    if not isinstance(nombre_archivo_py, Path):
        nombre_archivo_py = Path(nombre_archivo_py)

    dic_es_nombre   = f"es-{nombre_archivo_py.stem}.dic"
    dic_dest_nombre = f"{idioma}-{nombre_archivo_py.stem}.dic"

    # Cargar diccionarios
    dic_es   = cargar_diccionario(dic_es_nombre)
    dic_dest = cargar_diccionario(dic_dest_nombre)

    archivo_src = SRC_DIR / nombre_archivo_py
    if not archivo_src.exists():
        print(f"❌ No existe {archivo_src}")
        return False

    contenido = archivo_src.read_text(encoding="utf-8")

    # Primero vamos a poner correctamente el idioma para las fuentes
    # y luego modificamos matplotlib para que use Aggs y no abra ventanas
    c1 =f'idioma_actual = "es"'
    c1t = f'idioma_actual = "{idioma}"'
    c2 = f'#matplotlib.use("Agg")'
    c2t = 'matplotlib.use("Agg")'
    c3 = f'plt.show()'
    c3t = f'# plt.show()  # Desactivado en traducciones'
    contenido = contenido.replace(c1, c1t)
    contenido = contenido.replace(c2, c2t)
    contenido = contenido.replace(c3, c3t)


    # Aplicar traducciones solo si no es español
    if idioma != "es":
        contenido = aplicar_diccionario(contenido, dic_es, dic_dest)


    # Aplicar corregir_save para que los save/savefig tengan prefijo

    contenido = corregir_save(contenido, idioma)

    # Guardar temporal en TMP_DIR
    temporal = TMP_DIR / f"{idioma}_{nombre_archivo_py.name}"
    temporal.write_text(contenido, encoding="utf-8")

    # Ejecutar EL FICHERO (no el contenido)
    try:
        comando = str(temporal)
        runpy.run_path(comando, run_name="__main__")
    except Exception as e:
        print(f"❌ Error al ejecutar {temporal}: {e}")
        return False

    return True

def obtener_idiomas_para_py(nombre_archivo_py, incluir_es=False):
    patron = f"*-{nombre_archivo_py.stem}.dic"
    idiomas = []

    for dic in DIC_DIR.glob(patron):
        idioma = dic.name.split("-")[0]
        if idioma == "es" and not incluir_es:
            continue
        idiomas.append(idioma)

    return sorted(set(idiomas))


# ==============================
# MAIN
# ==============================

def main():
    import sys

    if len(sys.argv) < 3:
        print("Uso: python explorar.py archivo.py idioma [test]")
        print("     python explorar.py todos idioma [test]")
        print("     python explorar.py archivo.py todos [test]")
        print("     python explorar.py todos todos [test]")
        return

    arg_archivo_raw = sys.argv[1]
    arg_idioma_raw  = sys.argv[2]
    arg_archivo = arg_archivo_raw.lower()
    arg_idioma  = arg_idioma_raw.lower()
    
    test = len(sys.argv) > 3

    # Determina si es caso múltiple
    caso_multiple = (
        arg_archivo in ("todos", "todas", "all") or
        arg_idioma  in ("todos", "todas", "all", "tots", "todes")
    )

    # Archivos a procesar
    if arg_archivo in ("todos", "todas", "all"):
        archivos = list(SRC_DIR.glob("*.py"))
    else:
        archivos = [SRC_DIR / arg_archivo_raw]

    if not archivos:
        print("⚠️  No hay archivos para procesar")
        return

    # Función para construir ruta de diccionario
    def diccionario(py, idioma):
        return DIC_DIR / f"{idioma}-{py.stem}.dic"

    # Caso múltiple
    if caso_multiple:
        for py in archivos:

            dic_es = diccionario(py, "es")

            # Sin español no hay nada que hacer para este archivo
            if not dic_es.exists():
                print(f"⚠️  {py.name}: falta diccionario base {dic_es.name}")
                continue

            # Determinar idiomas a procesar
            if arg_idioma in ("todos", "todas", "all", "tots", "todes"):
                idiomas = obtener_idiomas_para_py(py)
            else:
                idiomas = [arg_idioma]

            # Quitar 'es' si ya está y añadirlo al final
            idiomas = [i for i in idiomas if i != "es"]
            idiomas.append("es")

            for idioma in idiomas:

                dic_id = diccionario(py, idioma)

                if not dic_id.exists():
                    print(f"⚠️  {py.name}: falta diccionario {dic_id.name}")
                    continue

                if test:
                    print(f"🧪 TEST: python {py.name} {idioma}")
                else:
                    print(f"🔧 PROCESANDO: {py.name} → {idioma.upper()}")
                    procesar_py(py, idioma)

        return

    # Caso simple
    py = SRC_DIR / arg_archivo_raw
    idioma = arg_idioma_raw

    dic_es = diccionario(py, "es")
    dic_id = diccionario(py, idioma)

    if not dic_es.exists():
        print(f"⚠️  {py.name}: falta diccionario base {dic_es.name}")
        return

    if not dic_id.exists():
        print(f"⚠️  {py.name}: falta diccionario {dic_id.name}")
        return

    if idioma == "essssss":
        print("⚠️  No tiene sentido traducir es → es")
        return

    print(f"🔧 PROCESANDO: {py.name} → {idioma.upper()}")
    procesar_py(py.name, idioma)


# =====================================
if __name__ == "__main__":
    main()