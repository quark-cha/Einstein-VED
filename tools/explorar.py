import os
import re
import runpy
from pathlib import Path
import glob


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

print(f"📂 Directorio base: {BASE_DIR}")
print(f"📂 SRC listo: {SRC_DIR}")
print(f"📂 TMP listo: {TMP_DIR}")
print(f"📂 IMG listo: {IMG_DIR}")
print(f"📂 Diccionarios: {DIC_DIR}")

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
    "jp": "JP_",
    "sk": "SK_"
}
# se excluye el chino ch

def obtener_prefijo(idioma):
    return PREFIJOS.get(idioma, "")

# ==============================
# LECTURA DE DICCIONARIOS .dic
# ==============================

def cargar_diccionario(archivo):
    dic_file = DIC_DIR / archivo
    if not dic_file.exists():
        print(f"[AVISO] No existe {dic_file}")
        return []
    pares = []
    with dic_file.open("r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            partes = linea.split(";")
            if len(partes) != 4:
                print(f"[ERROR] línea inválida en {dic_file}: {linea}")
                continue
            pares.append(partes)  # idioma;archivo;id;texto
    return pares

# ==============================
# APLICAR DICCIONARIOS - CORREGIDO
# ==============================

def aplicar_diccionario(contenido, dic_es, dic_dest):
    """
    Reemplaza TODAS las ocurrencias del texto español por su traducción.
    Cada línea en dic_es se corresponde con la misma línea en dic_dest.
    """
    contador_total = 0
    
    # Verificar que tenemos datos para trabajar
    if not dic_es or not dic_dest:
        print("  ⚠ Uno de los diccionarios está vacío")
        return contenido
    
    # Usar el tamaño del más pequeño
    n_lineas = min(len(dic_es), len(dic_dest))
    
    print(f"  📝 Procesando {n_lineas} pares de traducción...")
    
    for i in range(n_lineas):
        # Verificar que ambas líneas tienen el formato correcto
        if len(dic_es[i]) < 4 or len(dic_dest[i]) < 4:
            continue
        
        texto_es = dic_es[i][3]
        texto_traducido = dic_dest[i][3]
        
        # Solo reemplazar si hay texto y son diferentes
        if texto_es and texto_traducido and texto_es != texto_traducido:
            # Contar cuántas veces aparece
            ocurrencias = contenido.count(texto_es)
            if ocurrencias > 0:
                # Reemplazar TODAS las ocurrencias
                contenido = contenido.replace(texto_es, texto_traducido)
                contador_total += ocurrencias
                # Mostrar solo los primeros reemplazos para no saturar
                if i < 5:  # Muestra los primeros 5 reemplazos como ejemplo
                    print(f"    → '{texto_es[:40]}...' → {ocurrencias} vez(es)")
    
    print(f"  ✅ Total de reemplazos: {contador_total}")
    return contenido

# ==============================
# CORRECCIÓN SAVE → RUTA COMPLETA IMG CON PREFIJO
# ==============================

def corregir_save(contenido, prefijo):
    prefijo = prefijo.upper()
    
    patron = r'(save|savefig)\(\s*["\']([^"\']+)["\']'
    
    def reemplazo(m):
        func = m.group(1)
        archivo = m.group(2)
        archivo_pref = prefijo + archivo
        ruta_completa = os.path.join(str(IMG_DIR), archivo_pref)
        return f'{func}(r"{ruta_completa}"'  # mantenemos lo demás
       
    return re.sub(patron, reemplazo, contenido)

# ==============================
# COMPROBAR DICCIONARIOS
# ==============================

def comprobar_diccionarios(nombre_archivo_py, dic_es, dic_dest, idioma):
    lineas_es = len(dic_es)
    lineas_dest = len(dic_dest)

    print("\n📘 COMPROBACIÓN DE DICCIONARIOS")
    print(f"   Archivo PY: {nombre_archivo_py}")
    print(f"   Español (ES): {lineas_es} líneas")
    print(f"   {idioma.upper()}: {lineas_dest} líneas")

    if lineas_dest == lineas_es:
        print(f"   ✅ Diccionario {idioma.upper()} CORRECTO (mismas líneas)")
        return

    elif lineas_dest > lineas_es:
        print(f"   ❌ ERROR: Diccionario {idioma.upper()} TIENE LÍNEAS DE MÁS ({lineas_dest - lineas_es})")
        print("   → Revisa ese .dic, sobran entradas extrañas.")
        return

    else:
        faltan = lineas_es - lineas_dest
        print(f"   ⚠ INCOMPLETO: Faltan {faltan} traducciones básicas para {idioma.upper()}.")

        # Identificar qué IDs faltan
        ids_es = { fila[2] for fila in dic_es }
        ids_dest = { fila[2] for fila in dic_dest }

        ids_faltan = ids_es - ids_dest
        print("   → IDs faltantes:")
        for idf in sorted(ids_faltan):
            print("      -", idf)

# ==============================
# PROCESAR UN ARCHIVO
# ==============================

def procesar_py(nombre_archivo_py, idioma):
    dicionario = DIC_DIR / f"{idioma}-{nombre_archivo_py.replace('.py','.dic')}"
    archivo_src = SRC_DIR / nombre_archivo_py
    
    if not archivo_src.exists():
        print(f"❌ No existe {archivo_src}")
        return False
    
    if not dicionario.exists():
        print(f"❌ No existe diccionario {dicionario}")
        return False
    
    print(f"\n📄 Procesando: {archivo_src}")
    print(f"🌍 Idioma destino: {idioma.upper()}")
    print("-" * 50)
    
    dic_es_nombre = f"es-{nombre_archivo_py.replace('.py','.dic')}"
    dic_dest_nombre = f"{idioma}-{nombre_archivo_py.replace('.py','.dic')}"

    dic_es = cargar_diccionario(dic_es_nombre)
    dic_dest = cargar_diccionario(dic_dest_nombre)

    comprobar_diccionarios(nombre_archivo_py, dic_es, dic_dest, idioma)

    contenido = archivo_src.read_text(encoding="utf-8")   
    
    print("🔄 Aplicando traducciones...")
    contenido_mod = aplicar_diccionario(contenido, dic_es, dic_dest)

    prefijo = obtener_prefijo(idioma)
    contenido_mod = corregir_save(contenido_mod, prefijo)
    # Dividir en líneas, filtrar y unir de nuevo
    contenido_mod = "\n".join(
        linea for linea in contenido_mod.splitlines() if "plt.show()" not in linea
    )
    
    # ================================================
    # CORRECCIÓN COMPLETA PARA CARACTERES CHINOS
    # ================================================
    
    if idioma == "ch":
        # LISTA DE CARACTERES CHINOS QUE DEBEN SER REEMPLAZADOS
        caracteres_problematicos = {
            '，': ',',   # Coma china → coma normal
            '。': '.',   # Punto chino → punto normal
            '；': ';',   # Punto y coma chino
            '：': ':',   # Dos puntos chinos
            '（': '(',   # Paréntesis chino abrir
            '）': ')',   # Paréntesis chino cerrar
            '［': '[',   # Corchete chino abrir
            '］': ']',   # Corchete chino cerrar
            '｛': '{',   # Llave china abrir
            '｝': '}',   # Llave china cerrar
            '《': '<',   # Comillas chinas abrir
            '》': '>',   # Comillas chinas cerrar
            '「': "'",   # Comilla simple china abrir
            '」': "'",   # Comilla simple china cerrar
            '『': '"',   # Comilla doble china abrir
            '』': '"',   # Comilla doble china cerrar
        }
        
        print("🔠 Corrigiendo caracteres chinos en código...")
        
        # Reemplazar todos los caracteres problemáticos
        for chino, normal in caracteres_problematicos.items():
            if chino in contenido_mod:
                contenido_mod = contenido_mod.replace(chino, normal)
                print(f"   {chino} → {normal}")
    
    # ================================================
    # CONFIGURACIÓN BÁSICA PARA TODOS LOS IDIOMAS
    # ================================================
    
    # 1. Asegurar matplotlib.use('Agg') esté descomentado
    contenido_mod = contenido_mod.replace("#matplotlib.use('Agg')", "matplotlib.use('Agg')")
    
    # 2. Añadir encoding UTF-8 al inicio
    contenido_mod = f"# -*- coding: utf-8 -*-\n{contenido_mod}"
    
    # 3. Configuración de fuentes solo para chino
    if idioma == "ch":
        config_chino = "\n# Configuración para caracteres chinos\nimport matplotlib.pyplot as plt\nplt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']\nplt.rcParams['axes.unicode_minus'] = False\n"
        
        # Insertar después de la primera línea de import matplotlib
        if "import matplotlib" in contenido_mod:
            lineas = contenido_mod.split('\n')
            for i, linea in enumerate(lineas):
                if "import matplotlib" in linea and i+1 < len(lineas):
                    # Insertar después del import matplotlib
                    lineas.insert(i + 1, config_chino)
                    break
            contenido_mod = '\n'.join(lineas)
        else:
            # Añadir al principio si no hay import matplotlib
            contenido_mod = contenido_mod.replace("# -*- coding: utf-8 -*-\n")
    
    # ================================================
    # GUARDAR ARCHIVO TEMPORAL
    # ================================================
    
    tmp_file = TMP_DIR / f"{idioma}_{nombre_archivo_py}"
    
    try:
        # Verificar sintaxis ANTES de guardar
        import ast
        ast.parse(contenido_mod)
        
        tmp_file.write_text(contenido_mod, encoding="utf-8")
        print(f"📝 Temporal generado: {tmp_file}")
        print("✅ Sintaxis verificada (código válido)")
        
    except SyntaxError as e:
        print(f"⚠️  Error de sintaxis: {e}")
        
        # CORRECCIÓN DE EMERGENCIA: eliminar TODOS los caracteres no-ASCII del código
        print("🔄 Aplicando corrección de emergencia...")
        
        lineas = contenido_mod.split('\n')
        lineas_corregidas = []
        
        for linea in lineas:
            # Separar strings del código
            partes = []
            en_string = False
            string_delimiter = None
            current_part = ""
            
            for char in linea:
                if char in ('"', "'") and not en_string:
                    en_string = True
                    string_delimiter = char
                    if current_part:
                        partes.append(('code', current_part))
                    current_part = char
                elif char == string_delimiter and en_string:
                    en_string = False
                    current_part += char
                    partes.append(('string', current_part))
                    current_part = ""
                    string_delimiter = None
                else:
                    current_part += char
            
            if current_part:
                partes.append(('code' if not en_string else 'string', current_part))
            
            # Reconstruir línea: mantener strings intactos, limpiar código
            nueva_linea = ""
            for tipo, texto in partes:
                if tipo == 'code':
                    # En código: reemplazar caracteres problemáticos
                    texto = texto.replace('，', ',')
                    texto = texto.replace('。', '.')
                    texto = texto.replace('；', ';')
                    texto = texto.replace('：', ':')
                    texto = texto.replace('（', '(')
                    texto = texto.replace('）', ')')
                nueva_linea += texto
            
            lineas_corregidas.append(nueva_linea)
        
        contenido_mod = '\n'.join(lineas_corregidas)
        
        # Guardar versión corregida
        tmp_file.write_text(contenido_mod, encoding="utf-8")
        print("✅ Archivo corregido y guardado")
    
    # ================================================
    # EJECUTAR TEMPORAL
    # ================================================
    
    print("⚙️ Ejecutando temporal para generar imágenes...")
    try:
        runpy.run_path(str(tmp_file), run_name="__main__")
        # print(f"✅ Imágenes depositadas en: {IMG_DIR}")
        return True
    except Exception as e:
        # print(f"❌ Error ejecutando {tmp_file}: {e}")
        return False
    
import csv
# =====================================
# Cargar diccionarios españoles en memoria
# =====================================
def cargar_diccionario_espanol():
    dic_es = {}
    for ruta in DIC_DIR.glob("es-*.dic"):
        archivo = ruta.name[3:-4]  # quitar "es-" y ".dic"
        dic_es[archivo] = {}
        with ruta.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)  # saltar cabecera
            for fila in reader:
                if len(fila) < 4:
                    continue
                id_linea = fila[2].strip()
                texto_es = fila[3]
                dic_es[archivo][id_linea] = texto_es
    return dic_es


# =====================================
# Cargar diccionarios de otros idiomas existentes
# =====================================
def cargar_diccionarios_idiomas():
    dic_idiomas = {}
    for ruta in DIC_DIR.glob("*-*.dic"):
        if ruta.name.startswith("es-"):
            continue  # español ya cargado
        parts = ruta.name[:-4].split("-", 1)
        if len(parts) != 2:
            continue
        idioma, archivo = parts
        dic_idiomas.setdefault(idioma, {})[archivo] = {}
        with ruta.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for fila in reader:
                if len(fila) < 4:
                    continue
                id_linea = fila[2].strip()
                texto = fila[3]
                dic_idiomas[idioma][archivo][id_linea] = texto
    return dic_idiomas
import sys

def estadisticas_y_limpieza(dic_idiomas, dic_es):
    
    print("\n===== Estadísticas finales =====")
    
    # Primero mostrar todo sin borrar
    archivos_vacios = []
    
    # Crear lista de todos los elementos para ordenar
    elementos = []
    
    for idioma, archivos in dic_idiomas.items():
        for archivo, lineas in archivos.items():
            elementos.append((idioma, archivo, lineas))
    
    # Ordenar primero por archivo (sin extensión .py), luego por idioma
    elementos.sort(key=lambda x: (x[1].replace('.py', ''), x[0]))
    
    for idioma, archivo, lineas in elementos:
        archivo_sinpy = archivo.replace(".py", ".dic")
        total_es = len(dic_es.get(archivo, {}))
        total_idioma = len(lineas)
        test = "❌"
        if total_idioma == total_es:
            test = "✅"
        
        ruta_archivo = DIC_DIR / f"{idioma}-{archivo_sinpy}"
        ruta_absoluta = str(ruta_archivo.absolute())
        
        # Formatear ruta según SO
        if sys.platform.startswith('win'):
            # Probemos con dos puntos (más común)
            ruta_url = f"file:///{ruta_absoluta.replace('\\', '/')}"
            # O alternativamente sin file://, solo la ruta
            # ruta_url = ruta_absoluta
        else:
            # Unix/Linux/Mac: file:///ruta/archivo
            ruta_url = f"file://{ruta_absoluta}"
        
            
        #print(f"{test} {total_idioma:<4} {total_es:<5} {idioma:>8}-{archivo_sinpy}")
        ruta_archivo = ruta_url
        print(f"{test} {total_idioma:<4} {total_es:<5} \033]8;;{ruta_archivo}\033\\{idioma:>8}-{archivo_sinpy}\033]8;;\033\\")
    
        
        # Guardar archivos vacíos para preguntar después
        if total_es == 0:
            ruta_archivo = DIC_DIR / f"{idioma}-{archivo_sinpy}"
            print(f"{test} {total_idioma:<4} {total_es:<5} \033]8;;{ruta_archivo}\033\\{idioma:>8}-{archivo_sinpy}\033]8;;\033\\")    
            nombre_completo = f"{idioma}-{archivo_sinpy}"
            archivos_vacios.append(nombre_completo)
            print(f"Encontrado diccionario sin referencias al español {nombre_completo}")
    
    # Preguntar sobre archivos vacíos
    if archivos_vacios:
        print(f"\n⚠️  ENCONTRADOS {len(archivos_vacios)} ARCHIVO(S) VACÍO(S):")
        for nombre in archivos_vacios:
            print(f"  - {nombre}")
        
        respuesta = input(f"\n¿Eliminar estos {len(archivos_vacios)} archivo(s) vacíos? (sí/no): ").strip().lower()
        
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            borrados = 0
            for nombre in archivos_vacios:
                ruta = DIC_DIR / nombre
                try:
                    if ruta.exists():
                        ruta.unlink()
                        print(f"✅ Eliminado: {nombre}")
                        borrados += 1
                except Exception as e:
                    print(f"❌ Error con {nombre}: {e}")
            print(f"\n📊 Borrados: {borrados} de {len(archivos_vacios)} archivos.")
        else:
            print("❌ Operación cancelada.")
    
    limpiar_parametros_tecnicos(modo_seguro=True)  # Pide confirmación
    eliminados = limpiar_diccionarios_huérfanos()
    print (f"Se eliinaron diccionarios huerfanos {eliminados}")   
    return


def limpiar_diccionarios_huérfanos():
    """
    Elimina archivos .dic en DIC_DIR que no tienen su archivo .py correspondiente en SRC_DIR.
    Formato requerido: <idioma>-<fichero>.dic → busca <fichero>.py en SRC_DIR
    
    Variables globales requeridas:
    - DIC_DIR: Ruta al directorio con archivos .dic
    - SRC_DIR: Ruta al directorio con archivos .py
    """
    eliminados = []
    
    try:
        # Verificar que las variables globales existen
        if 'DIC_DIR' not in globals() or 'SRC_DIR' not in globals():
            print("⚠️  Error: DIC_DIR o SRC_DIR no están definidas como variables globales")
            return eliminados
        
        # Verificar que los directorios existen
        if not os.path.exists(DIC_DIR):
            print(f"⚠️  Directorio DIC_DIR no existe: {DIC_DIR}")
            return eliminados
        
        if not os.path.exists(SRC_DIR):
            print(f"⚠️  Directorio SRC_DIR no existe: {SRC_DIR}")
            return eliminados
        
        print(f"🧹 Limpiando diccionarios huérfanos...")
        print(f"• DIC_DIR: {DIC_DIR}")
        print(f"• SRC_DIR: {SRC_DIR}")
        print("-" * 50)
        
        # Buscar todos los archivos .dic
        archivos_dic = glob.glob(os.path.join(DIC_DIR, "*.dic"))
        
        if not archivos_dic:
            print("📭 No se encontraron archivos .dic")
            return eliminados
            
        print(f"🔍 Encontrados {len(archivos_dic)} archivos .dic")
        
        # Procesar cada archivo .dic
        for ruta_dic in archivos_dic:
            nombre_dic = os.path.basename(ruta_dic)
            
            # Validar formato: <idioma>-<fichero>.dic
            if '-' not in nombre_dic or not nombre_dic.endswith('.dic'):
                print(f"⚠️  Formato inválido (se espera idioma-fichero.dic): {nombre_dic}")
                continue
            
            # Extraer el nombre del fichero base
            partes = nombre_dic.rsplit('-', 1)
            if len(partes) != 2:
                continue
                
            nombre_base = partes[1][:-4]  # Quitar .dic
            nombre_py = f"{nombre_base}.py"
            ruta_py = os.path.join(SRC_DIR, nombre_py)
            
            # Verificar si existe el .py correspondiente
            if os.path.exists(ruta_py):
                print(f"✓ {nombre_dic} → {nombre_py} (OK)")
            else:
                print(f"❌ {nombre_dic} → {nombre_py} (NO EXISTE)")
                try:
                    os.remove(ruta_dic)
                    eliminados.append(nombre_dic)
                    print(f"  🗑️  Eliminado: {nombre_dic}")
                except Exception as e:
                    print(f"  ⚠️  Error al eliminar: {e}")
        
        # Resumen
        print("-" * 50)
        if eliminados:
            print(f"✅ Se eliminaron {len(eliminados)} diccionarios huérfanos:")
            for dic in eliminados:
                print(f"  • {dic}")
        else:
            print("🎉 No se encontraron diccionarios huérfanos")
            
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
    
    return eliminados

def limpiar_parametros_tecnicos(modo_seguro=True):
    """
    Busca y elimina parámetros técnicos con confirmación.
    """
    print("🧹 LIMPIEZA DE PARÁMETROS TÉCNICOS")
    print("=" * 60)
    
    patrones_tecnicos = {
        'upper right', 'upper left', 'lower right', 'lower left',
        'right', 'center left', 'center right', 'lower center',
        'upper center', 'center', 'best',
        'round,pad=0.3', 'round,pad=0.5', 'round,pad=0.6', 'round,pad=0.8',
        'round,pad=1.0',
        'k--', 'k-', 'b--', 'r--', 'g--', 'y--', 'm--', 'c--',
        'solid', 'dashed', 'dotted', 'dashdot',
        'None', 'True', 'False',
    }
    
    diccionarios_es = list(DIC_DIR.glob("es-*.dic"))
    
    if not diccionarios_es:
        print("❌ No se encontraron diccionarios españoles")
        return
    
    total_encontrados = 0
    total_a_eliminar = 0
    resumen = []
    
    # PRIMERA PASADA: Detectar y mostrar
    print("\n📋 DETECCIÓN DE PARÁMETROS TÉCNICOS:")
    print("-" * 40)
    
    for dic_es_path in diccionarios_es:
        nombre_base = dic_es_path.name[3:]
        encontrados_en_archivo = []
        
        with dic_es_path.open('r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            cabecera = next(reader, None)
            
            for fila in reader:
                if len(fila) < 4:
                    continue
                
                id_linea = fila[2].strip()
                texto_es = fila[3].strip()
                
                if texto_es in patrones_tecnicos:
                    encontrados_en_archivo.append((id_linea, texto_es))
        
        if encontrados_en_archivo:
            total_encontrados += len(encontrados_en_archivo)
            resumen.append((dic_es_path, encontrados_en_archivo))  # <-- GUARDAR Path, no string
            
            print(f"\n📄 {dic_es_path.name}:")
            for id_linea, texto in encontrados_en_archivo:
                print(f"   ⚠️  ID {id_linea}: '{texto}'")
    
    if total_encontrados == 0:
        print("\n✅ No se encontraron parámetros técnicos")
        return
    
    # MOSTRAR RESUMEN
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN: {total_encontrados} parámetros técnicos encontrados")
    print("=" * 60)
    
    # PREGUNTAR CONFIRMACIÓN
    if modo_seguro:
        print("\n⚠️  ¿Deseas eliminar estos parámetros técnicos?")
        print("   Se eliminarán de TODOS los diccionarios correspondientes")
        print("\nOpciones:")
        print("  1. Sí, eliminar TODO")
        print("  2. Sí, pero mostrar cada archivo antes")
        print("  3. No, cancelar")
        print("  4. Mostrar lista completa primero")
        
        while True:
            try:
                opcion = input("\n👉 Tu opción (1-4): ").strip()
                
                if opcion == '1':
                    confirmar = input("¿ESTÁS SEGURO? (sí/no): ").strip().lower()
                    if confirmar in ['s', 'si', 'sí', 'y', 'yes']:
                        print("\n🔄 Eliminando...")
                        break
                    else:
                        print("❌ Cancelado")
                        return
                        
                elif opcion == '2':
                    modo_confirmacion_detallada = True
                    break
                    
                elif opcion == '3':
                    print("❌ Operación cancelada")
                    return
                    
                elif opcion == '4':
                    print("\n📋 LISTA COMPLETA A ELIMINAR:")
                    print("-" * 40)
                    for archivo_path, items in resumen:
                        print(f"\n{archivo_path.name}:")
                        for id_linea, texto in items:
                            print(f"  - ID {id_linea}: '{texto}'")
                    print("\n" + "=" * 40)
                    continue
                    
                else:
                    print("❌ Opción inválida")
                    
            except KeyboardInterrupt:
                print("\n❌ Cancelado por el usuario")
                return
    
    # SEGUNDA PASADA: Eliminar (si se confirmó)
    print("\n🔄 ELIMINANDO PARÁMETROS TÉCNICOS...")
    
    for dic_es_path, items in resumen:  # <-- dic_es_path es un Path
        nombre_base = dic_es_path.name[3:]  # quitar "es-"
        ids_a_eliminar = {id_linea for id_linea, _ in items}
        
        if modo_seguro and 'modo_confirmacion_detallada' in locals():
            print(f"\n📄 {dic_es_path.name}: {len(items)} items")
            respuesta = input(f"   ¿Eliminar? (sí/no/todos): ").strip().lower()
            if respuesta in ['no', 'n']:
                print("   ⏭️  Saltando este archivo")
                continue
            elif respuesta == 'todos':
                modo_confirmacion_detallada = False
        
        # Eliminar de español
        with dic_es_path.open('r', encoding='utf-8') as f:
            lineas = list(csv.reader(f, delimiter=';'))
        
        if lineas:
            cabecera = lineas[0]
            lineas_limpias = [linea for linea in lineas[1:] 
                            if len(linea) < 4 or linea[2].strip() not in ids_a_eliminar]
            
            with dic_es_path.open('w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(cabecera)
                writer.writerows(lineas_limpias)
        
        # Eliminar de otros idiomas
        eliminados_en_archivo = 0
        for idioma in ['ar', 'ch', 'de', 'en', 'fr', 'it', 'sk']:
            dic_path = DIC_DIR / f"{idioma}-{nombre_base}"
            if not dic_path.exists():
                continue
            
            with dic_path.open('r', encoding='utf-8') as f:
                lineas = list(csv.reader(f, delimiter=';'))
            
            if lineas:
                cabecera = lineas[0]
                lineas_limpias = [linea for linea in lineas[1:]
                                if len(linea) < 4 or linea[2].strip() not in ids_a_eliminar]
                
                eliminados = len(lineas) - len(lineas_limpias) - 1  # -1 por cabecera
                eliminados_en_archivo += eliminados
                
                with dic_path.open('w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerow(cabecera)
                    writer.writerows(lineas_limpias)
        
        total_a_eliminar += eliminados_en_archivo
        print(f"   ✅ {dic_es_path.name}: {len(items)} IDs, {eliminados_en_archivo} líneas eliminadas")
    
    print("\n" + "=" * 60)
    print(f"✅ LIMPIEZA COMPLETADA")
    print(f"📊 Total líneas eliminadas: {total_a_eliminar}")
    print(f"📁 Archivos procesados: {len(resumen)}")    
# ==============================
# MAIN
# ==============================

def main():
    import sys

    if len(sys.argv) == 1:
        print("Uso: python explorar.py archivo.py idioma")
        print("     python explorar.py archivo.py todos  (para todos los idiomas)")
        print("     python explorar.py todos idioma      (para todos los archivos)")
        print("     python explorar.py todos todos       (para absolutamente todo)")
        return
    elif len(sys.argv) == 2:
        idioma = "en"  # Por defecto
    elif len(sys.argv) == 3:
        idioma = sys.argv[2]

    arg_archivo = sys.argv[1]
    
    # Determinar archivos .py a procesar
    if arg_archivo.lower() in ["todos", "todas"]:
        archivos_py = [p.name for p in SRC_DIR.glob("*.py") if p.name != "explorar.py"]
    else:
        archivos_py = [arg_archivo]
    
    # Determinar idiomas a procesar
    if idioma.lower() in ["todos", "todas", "all", "tots", "todes"]:
        # Todos los idiomas disponibles (excluyendo español si lo deseas)
        idiomas_a_procesar = [idioma for idioma in PREFIJOS.keys() if idioma != "es"]
    else:
        # Un solo idioma específico
        idiomas_a_procesar = [idioma]
    
    # MODO TEST - estadísticas
    if arg_archivo.lower() in ["test"]:
        dic_idiomas = cargar_diccionarios_idiomas()
        dic_es = cargar_diccionario_espanol()
        print("ANALISIS DE DICCIONARIOS:")
        estadisticas_y_limpieza(dic_idiomas, dic_es)
        return
    
    total = 0
    # Procesar combinaciones: (archivo.py × idioma)
    for py in archivos_py:
        for idioma_actual in idiomas_a_procesar:
            print(f"\n{'='*60}")
            print(f"🔧 PROCESANDO: {py} → {idioma_actual.upper()}")
            print(f"{'='*60}")
            
            exito = procesar_py(py, idioma_actual)
            if exito:
                total += 1
    
    print(f"\n{'='*60}")
    print(f"🎯 PROCESO COMPLETADO")
    print(f"{'='*60}")
    
    if len(archivos_py) == 1 and len(idiomas_a_procesar) == 1:
        print(f"📊 Archivo procesado: {archivos_py[0]}")
        print(f"🌍 Idioma destino: {idiomas_a_procesar[0]}")
    elif len(archivos_py) > 1 and len(idiomas_a_procesar) == 1:
        print(f"📊 Archivos procesados: {len(archivos_py)}")
        print(f"🌍 Idioma destino: {idiomas_a_procesar[0]}")
    elif len(archivos_py) == 1 and len(idiomas_a_procesar) > 1:
        print(f"📊 Archivo procesado: {archivos_py[0]}")
        print(f"🌍 Idiomas destino: {len(idiomas_a_procesar)} ({', '.join(idiomas_a_procesar)})")
    else:
        print(f"📊 Archivos procesados: {len(archivos_py)}")
        print(f"🌍 Idiomas destino: {len(idiomas_a_procesar)}")
    
    print(f"✅ Procesos exitosos: {total}/{(len(archivos_py) * len(idiomas_a_procesar))}")
    print(f"📂 Archivos temporales en: {TMP_DIR}")
    print(f"🖼️  Imágenes en: {IMG_DIR}")
    
if __name__ == "__main__":
    main()