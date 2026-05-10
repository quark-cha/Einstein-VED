Sistema de Internacionalización de Gráficas
Objetivo
Generar automáticamente versiones multilingües de scripts Python que producen gráficas, manteniendo un diccionario centralizado para traducciones.

Estructura
text
DIR_BASE/
├── SRC/           # Scripts Python originales (en español)
├── tmp/           # Scripts temporales generados por idioma
├── img/           # Gráficas con prefijo idiomático
└── DIC/           # Diccionarios antiguos
Flujo de Procesamiento
1. Extracción de Textos
Analiza scripts .py en SRC/

Excluye docstrings, comentarios, rutas y palabras protegidas

Genera diccionario base: <idioma>;<id-general>;<texto>

2. Generación por Idioma
Crea versiones traducidas de cada script

Añade prefijos idiomáticos (ES_grafica.png, EN_grafica.png)

Ejecuta en paralelo

3. Gestión de Diccionarios
Mantiene compatibilidad con diccionarios antiguos

Marca con * entradas que necesitan revisión

Estado Actual ✅
Funcionalidades Implementadas
Detección y Creación de Diccionario

Extracción robusta de textos de scripts Python

Generación inicial de diccionario español

Exclusión inteligente de contenido no traducible

Sistema de Traducción

Sustitución contextual en código Python

Preservación de rutas, formatos y términos técnicos

Generación de scripts temporales por idioma

Gestión de Gráficas

Prefijos idiomáticos automáticos

Movimiento organizado al directorio img/

Múltiples formatos (PNG, JPG, SVG, PDF, EPS)

Monitorización

Sistema completo de alertas visuales

Registro detallado de operaciones

Manejo elegante de errores

Próximos Pasos 🚧
Restauración de Diccionario Obsoleto

Comparar diccionario actual con versión antigua

Identificar textos modificados o nuevos

Marcar entradas que requieren retraducción

Características Técnicas
Formatos Soportados
Scripts: Python (.py)

Imágenes: PNG, JPG, JPEG, SVG, GIF, PDF, EPS

Diccionarios: CSV con separador ;

Palabras Protegidas
Excluye automáticamente términos técnicos, colores, formatos y valores booleanos.

Uso
bash
python explorar.py
Archivos
diccionario.csv
text
es;script1_001;Título de la gráfica
en;script1_001;Chart title
fr;script1_001;Titre du graphique
Logs
explora-0.log: Log principal (rota a explora-1.log >4KB)

error.log: Errores críticos

Fortalezas
✅ Robusto: Manejo elegante de errores

✅ Escalable: Procesamiento paralelo

✅ Mantenible: Código modular

✅ Seguro: Exclusión de modificación manual

✅ Flexible: Múltiples idiomas y formatos

Sistema operacional y productivo - cualquier modificación debe preservar estas características.

import debugpy
import os
import csv
import re
import subprocess
from multiprocessing import Process
from datetime import datetime
import shutil
import glob

# =========================================================
# === CONFIGURACIÓN BÁSICA ================================
# =========================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_BASE = os.path.dirname(SCRIPT_DIR)
DIR_SRC = os.path.join(DIR_BASE, "SRC")
DIR_TMP = os.path.join(DIR_BASE, "tmp")
DIR_IMG = os.path.join(DIR_BASE, "img")
os.makedirs(DIR_TMP, exist_ok=True)
os.makedirs(DIR_IMG, exist_ok=True)

DICCIONARIO = os.path.join(DIR_SRC, "diccionario.csv")

# =========================================================
# === LOG Y SISTEMA DE ALERTAS ============================
# =========================================================
LOG_FILE = os.path.join(SCRIPT_DIR, "explora-0.log")
LOG_MAX_SIZE = 4096  # bytes
nivel_alerta = 1  # solo mensajes <= nivel se imprimen en consola

ALERTA_COLOR = {
    0: "\033[95m",  # malva claro (información)
    1: "\033[92m",  # verde (aviso)
    2: "\033[93m",  # amarillo (alerta relevante)
    3: "\033[91m",  # rojo (error)
}

def alerta(nivel, mensaje):
    global nivel_alerta, LOG_FILE

    # rollover log si supera 4KB
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > LOG_MAX_SIZE:
        old_log = os.path.join(SCRIPT_DIR, "explora-1.log")
        if os.path.exists(old_log):
            os.remove(old_log)
        os.rename(LOG_FILE, old_log)

    # escribir en log
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        fecha = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
        f.write(f"{fecha};{nivel};{mensaje}\n")

    # imprimir en consola solo si nivel <= nivel_alerta
    if nivel <= nivel_alerta:
        color = ALERTA_COLOR.get(nivel, "")
        print(f"{color}{mensaje}")
        
    # si nivel 3, escribir en fichero error.log con append
    if nivel == 3:
        ferror = os.path.join(SCRIPT_DIR,"error.log")
        with open(ferror, "a", encoding="utf-8") as f:
            f.write(f"{mensaje}\n")

# NUEVA FUNCIÓN: alarma
def alarma(mensaje):
    """
    Función de alarma para eventos importantes.
    Siempre se imprime en consola y se guarda en log como nivel 1.
    """
    alerta(1, f"[ALERTA IMPORTANTE] {mensaje}")

# =========================================================
# === LISTA DE PALABRAS PROTEGIDAS =======================
# =========================================================
PALABRAS_PROTEGIDAS = {
    "red", "blue", "green", "yellow", "orange", "brown", "gray",
    "black", "white", "lightgreen", "viridis", "plasma", "inferno",
    "center", "lower", "upper", "bold", "round", "tight", "auto", "off",
    "svg", "png", "jpg", "jpeg", "pdf", "True", "False", "None"
}

# =========================================================
# === FUNCIONES ===========================================
# =========================================================
def cargar_diccionario():
    if not os.path.exists(DICCIONARIO):
        alerta(2, "No existe diccionario.csv, se creará con textos base en español.")
        alarma("Diccionario inicial inexistente: se va a crear uno nuevo")
        return {}
    dic = {}
    with open(DICCIONARIO, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        for fila in reader:
            if len(fila) < 3:
                continue
            lang, id_texto, texto = fila[0].strip(), fila[1].strip(), fila[2].strip()
            if id_texto not in dic:
                dic[id_texto] = {}
            dic[id_texto][lang] = texto
    alerta(1, f"Diccionario cargado con {len(dic)} entradas")
    alarma(f"Diccionario cargado correctamente: {len(dic)} entradas")
    return dic

def obtener_idiomas(diccionario):
    idiomas = set()
    for traducciones in diccionario.values():
        idiomas.update(traducciones.keys())
    return sorted(list(idiomas))

def extraer_textos_espanol(filepath):
    textos = []
    dentro_docstring = False
    extensiones = (".png", ".jpg", ".jpeg", ".svg", ".gif", ".csv")
    with open(filepath, "r", encoding="utf-8") as f:
        for linea in f:
            linea_ext = linea.rstrip("\n")
            # Saltar docstrings
            if '"""' in linea or "'''" in linea:
                dentro_docstring = not dentro_docstring
                continue
            if dentro_docstring or linea.strip().startswith("#"):
                continue
            # Omitir plt.savefig
            if "plt.savefig" in linea:
                continue
            # Omitir archivos de imagen
            if any(ext in linea for ext in extensiones):
                continue
            # Buscar textos entre comillas normales
            matches = re.findall(r'(?<!\\)"([^"]+)"|(?<!\\)\'([^\']+)\'', linea)
            for m in matches:
                texto = m[0] or m[1]
                if texto.strip() and not texto.strip().isdigit():
                    textos.append(texto.strip())
    return textos

def crear_diccionario_si_no_existe():
    if os.path.exists(DICCIONARIO):
        alerta(1, f"Diccionario existente encontrado: {DICCIONARIO}")
        return cargar_diccionario()
    alerta(1, "Creando diccionario base (solo español)...")
    alarma("Creando diccionario inicial")
    dic = {}
    contador = 1
    for archivo in os.listdir(DIR_SRC):
        if "explorar" in archivo:
            alerta(1, f"Archivo {archivo} omitido para no incluir en el diccionario")
            continue
        if archivo.endswith(".py"):
            ruta = os.path.join(DIR_SRC, archivo)
            textos = extraer_textos_espanol(ruta)
            for texto in textos:
                id_texto = f"{os.path.splitext(archivo)[0]}_{contador:03d}"
                dic[id_texto] = {"es": texto}
                contador += 1
    with open(DICCIONARIO, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        for id_texto, traducciones in dic.items():
            writer.writerow(["es", id_texto, traducciones["es"]])
    alerta(0, f"Diccionario creado con {len(dic)} entradas en español.")
    alarma(f"Diccionario creado con {len(dic)} entradas en español")
    return dic

def traducir_linea(linea, idioma, diccionario):
    # ✅ EXCLUSIÓN TOTAL: Cualquier línea que contenga .savefig
    if ".savefig" in linea.lower():
        return linea
    
    # ✅ EXCLUSIÓN: Líneas con extensiones de imagen
    extensiones = (".png", ".jpg", ".jpeg", ".svg", ".gif", ".pdf", ".eps")
    if any(ext in linea for ext in extensiones):
        return linea
    
    # ✅ EXCLUSIÓN: Líneas con rutas (contienen / o \)
    if "/" in linea or "\\" in linea:
        return linea
    
    # Solo traducir el resto
    for id_texto, traducciones in diccionario.items():
        if "es" not in traducciones:
            continue
        texto_es = traducciones["es"]
        if texto_es in PALABRAS_PROTEGIDAS:
            continue
        if texto_es in linea:
            texto_idioma = traducciones.get(idioma, texto_es)
            linea = linea.replace(texto_es, texto_idioma)
    return linea


def generar_cola_mover_imagenes(idioma: str) -> str:
    """
    COLA: Mueve todas las imágenes con prefijo idiomático al DIR_IMG
    """
    return f"""
# Mover imágenes y poner prefijo {idioma.upper()}_

extensiones = ['*.png', '*.jpg', '*.jpeg', '*.svg', '*.gif', '*.pdf', '*.eps']
movidas = 0

for patron in extensiones:
    for archivo in glob.glob(patron):
        if os.path.isfile(archivo):
            try:
                # Crear nuevo nombre con prefijo
                nuevo_nombre = f"{idioma.upper()}_{{archivo}}"
                destino = os.path.join(DIR_IMG, nuevo_nombre)
                
                # Mover archivo
                shutil.move(archivo, destino)
                print(f"Movido: {{archivo}} -> {{destino}}")
                movidas += 1
            except Exception as e:
                print(f"Error moviendo {{archivo}}: {{e}}")

print(f"Total imágenes movidas: {{movidas}}")
"""

def ejecutar_script(path):
    try:
        subprocess.run(["python", path], check=True)
    except subprocess.CalledProcessError as e:
        alerta(3, f"Error ejecutando {path}: {e}. Ejecutar manualmente.")
        alarma(f"Error ejecutando script temporal: {path}")

def generar_tmp_scripts(diccionario, idioma):
    alerta(1, f"Generando scripts temporales para idioma: {idioma}")
    alarma(f"Iniciando generación de scripts temporales para {idioma}")
    procesos = []

    for root, _, files in os.walk(DIR_SRC):
        for archivo in files:
            if not archivo.endswith(".py"):
                continue
            if "explorar" in archivo:
                continue
            ruta = os.path.join(root, archivo)
            with open(ruta, "r", encoding="utf-8") as f:
                lineas = f.readlines()

            # Traducir (CON EXCLUSIÓN TOTAL de savefig)
            codigo_traducido = "".join(traducir_linea(linea, idioma, diccionario) for linea in lineas)

            # eliminar matplotlib
            lineas_traducido = [l for l in codigo_traducido.splitlines() if "matplotlib" not in l]
            codigo_traducido = "\n".join(lineas_traducido)

            # eliminar plt.show
            codigo_traducido = re.sub(r'plt\.show\s*\(\s*\)', '', codigo_traducido)
            
            # Cabecera segura
            cabecera  = "# AUTOGENERADO - NO MODIFICAR MANUALMENTE\n"
            cabecera += "import matplotlib\n"
            cabecera += "matplotlib.use('Agg')\n"
            cabecera += "import matplotlib.lines as mlines\n"
            cabecera += "import matplotlib.collections as collections\n"
            cabecera += "import matplotlib.patches as patches\n"
            cabecera += "from matplotlib.patches import Circle\n"
            cabecera += "from matplotlib import rcParams\n"
            cabecera += "from matplotlib.animation import FuncAnimation\n"
            cabecera += "import matplotlib.gridspec as gridspec\n"
            cabecera += "import matplotlib.pyplot as plt\n"
            cabecera += "import os\n"
            cabecera += "import glob\n"
            cabecera += "import shutil\n"
            
            cabecera += "plt.ioff()\n"
            cabecera += "plt.close('all')\n"           
            
            cabecera += f"DIR_IMG = r'{DIR_IMG}'\n"
            cabecera += f"IDIOMA = '{idioma.upper()}'\n\n"

            # ✅ AÑADIR COLA PARA MOVER IMÁGENES
            cola = generar_cola_mover_imagenes(idioma)
            codigo_completo = cabecera 
            codigo_completo += codigo_traducido
            codigo_completo += codigo_traducido + "\n\n" 
            codigo_completo += cola

            out_path = os.path.join(DIR_TMP, f"{idioma}_{os.path.basename(ruta)}")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(codigo_completo)
            
            alerta(0, f"✅ Script temporal generado: {out_path}")
            alarma(f"Script temporal listo: {out_path}")

            # ejecutar en subproceso
            p = Process(target=ejecutar_script, args=(out_path,))
            p.start()
            procesos.append(p)

    for p in procesos:
        p.join(timeout=100)
        if p.is_alive():
            alerta(3, f"Proceso atascado: {p.name}. Se finaliza manualmente.")
            alarma(f"Proceso atascado: {p.name}")
            p.terminate()
            p.join()

def ejecutar_tmp_scripts(idioma):
    alerta(1, f"Ejecutando scripts traducidos al {idioma}...")
    alarma(f"Iniciando ejecución de scripts para idioma {idioma}")
    for archivo in os.listdir(DIR_TMP):
        if "explorar" in archivo:
            continue
        if archivo.endswith(f"_{idioma}.py"):
            ruta = os.path.join(DIR_TMP, archivo)
            alerta(1, f"Ejecutando {archivo}")
            try:
                subprocess.run(["python", ruta], check=False)
                alerta(4,ruta)
            except subprocess.CalledProcessError as e:
                alerta(3, f"Error ejecutando script temporal {archivo}: {e}. Ejecutar manualmente.")
                alarma(f"Error ejecutando script temporal {archivo}")

# =========================================================
# === MARCAR ASTERISCOS EN VIEJO =========================
# =========================================================
def marcar_asteriscos_viejo(diccionario_nuevo):
    dic_viejo_path = os.path.join(DIR_BASE, "DIC", "diccionario.csv")
    if not os.path.exists(dic_viejo_path):
        alerta(2, f"No se encuentra diccionario viejo en DIC: {dic_viejo_path}. No se puede marcar *.")
        alarma(f"No se encuentra diccionario viejo: {dic_viejo_path}")
        return

    alerta(1, f"Cargando diccionario viejo desde {dic_viejo_path}...")
    viejo = []
    with open(dic_viejo_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        for fila in reader:
            if len(fila) < 3:
                continue
            viejo.append(fila)  # [idioma, id, texto]

    tmp_path = os.path.join(DIR_TMP, "tmp-diccionario.csv")
    shutil.copy(dic_viejo_path, tmp_path)

    idiomas_viejo = set(fila[0] for fila in viejo if fila[0] != "es")
    nuevo_ids = list(diccionario_nuevo.keys())
    nuevo_viejo = []
    idx_nuevo = 0

    for fila in viejo:
        idioma, id_v, texto = fila
        if idioma == "es":
            nuevo_viejo.append(fila)
            continue
        if idx_nuevo < len(nuevo_ids):
            id_n = nuevo_ids[idx_nuevo]
            texto_n = diccionario_nuevo[id_n]["es"]
            if texto == texto_n:
                nuevo_viejo.append([idioma, id_n, texto])
                idx_nuevo += 1
            else:
                nuevo_viejo.append([idioma, "*", texto])
        else:
            nuevo_viejo.append([idioma, "*", texto])

    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        for fila in nuevo_viejo:
            writer.writerow(fila)

    alerta(0, f"Comprobación completada. tmp-diccionario.csv generado en {tmp_path}.")
    alarma("Revisión del diccionario viejo completada, tmp-diccionario.csv listo")
    alerta(0, "Continuaremos desde aquí tras la verificación manual.")
    exit()

def limpiar_tmp():
    # =========================================================
    # === LIMPIEZA DEL DIRECTORIO TEMPORAL ====================
    # =========================================================
    if os.path.exists(DIR_TMP) and os.path.isdir(DIR_TMP):
        try:
            shutil.rmtree(DIR_TMP)
            alerta(1, f"Directorio temporal {DIR_TMP} eliminado completamente.")
        except Exception as e:
            alerta(3, f"No se pudo eliminar {DIR_TMP}: {e}")
    os.makedirs(DIR_TMP, exist_ok=True)
    alerta(1, f"Directorio temporal {DIR_TMP} recreado vacío.")

    
def preparar_diccionario_para_revision(diccionario):
    """
    Escribe el diccionario actual a un archivo temporal para inspección manual.
    No modifica el diccionario viejo ni altera ninguna funcionalidad existente.
    """
    tmp_dic_path = os.path.join(DIR_TMP, "tmp-diccionario.csv")
    with open(tmp_dic_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        for id_texto, traducciones in diccionario.items():
            es_texto = traducciones.get("es", "")
            writer.writerow(["es", id_texto, es_texto])

    alerta(1, f"Diccionario escrito en temporal para revisión: {tmp_dic_path}")
    alerta(0, f"Diccionario temporal para revisión creado en {tmp_dic_path}.")
    alarma(f"Diccionario listo para inspección manual: {tmp_dic_path}")

    return tmp_dic_path

    
# =========================================================
# === PROGRAMA PRINCIPAL ==================================
# =========================================================
def main():
    limpiar_tmp()
    alerta(0, "=== explorar.py — Sistema multilingüe ===")
    diccionario = crear_diccionario_si_no_existe()
    preparar_diccionario_para_revision(diccionario)  # <-- Genera tmp-diccionario.csv
    idiomas = obtener_idiomas(diccionario)
    alerta(0, f"Idiomas detectados en el diccionario: {', '.join(idiomas)}")
    alarma(f"Idiomas detectados: {', '.join(idiomas)}")

    español = 1
    # Continuar con todos los idiomas
    for idioma in idiomas:
        if español < 2:
            español = 0
            generar_tmp_scripts(diccionario, idioma)
            ejecutar_tmp_scripts(idioma)
            marcar_asteriscos_viejo(diccionario)

        generar_tmp_scripts(diccionario, idioma)
        ejecutar_tmp_scripts(idioma)
        
    alerta(0, "🏁 Finalizado.")
    alarma("Fin del proceso completo en explorar.py")

if __name__ == "__main__":
    main()