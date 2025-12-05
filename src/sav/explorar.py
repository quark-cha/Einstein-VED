import os
import csv
import glob
import subprocess
import shutil

# ============================================
# BASE: ruta del script (no del cwd)
# ============================================
BASE = os.path.dirname(os.path.abspath(__file__))

# Or using os.path
TMP_DIR = os.path.join(BASE, "..", "tmp")
os.makedirs(TMP_DIR, exist_ok=True)

print(f"📂 Directorio del script: {BASE}")
print(f"📂 TMP listo: {TMP_DIR}")
print(f"📂 Directorio de ejecución (cwd): {os.getcwd()}")

# ============================================================
# CARGAR DICCIONARIO POR TEXTO
# ============================================================
def cargar_diccionario_por_texto():
    diccionario = {}
    ruta_diccionario = os.path.join(BASE, "diccionario.csv")

    if not os.path.exists(ruta_diccionario):
        print("❌ ERROR: diccionario.csv no existe.")
        return diccionario

    try:
        with open(ruta_diccionario, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for fila in reader:
                if len(fila) < 4:
                    continue
                idioma = fila[0].strip()
                archivo = fila[1].strip()
                id_texto = fila[2].strip()
                texto = fila[3].strip()
                if idioma == "es":
                    diccionario[texto] = {"archivo": archivo, "id": id_texto, "traducciones": {}}
                else:
                    for texto_es, info in diccionario.items():
                        if info["archivo"] == archivo and info["id"] == id_texto:
                            info["traducciones"][idioma] = texto
                            break
    except Exception as e:
        print("❌ Error cargando diccionario:", e)

    return diccionario

# ============================================================
# TRADUCIR POR TEXTO
# ============================================================
def traducir_por_texto(texto_original, diccionario, idioma_destino):
    if texto_original in diccionario:
        return diccionario[texto_original]['traducciones'].get(idioma_destino, texto_original)
    return texto_original

# ============================================================
# EXTRAER TEXTOS DE ARCHIVO PYTHON
# ============================================================
def extraer_textos_archivo(ruta_archivo):
    textos = []
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        for comilla in ['"', "'"]:
            i = 0
            while i < len(contenido):
                if contenido[i] == comilla:
                    start = i + 1
                    i += 1
                    while i < len(contenido) and contenido[i] != comilla:
                        i += 1
                    if i < len(contenido):
                        texto = contenido[start:i].strip()
                        if len(texto) >= 3 and any(c.isalpha() for c in texto):
                            textos.append(texto)
                        i += 1
                else:
                    i += 1
    except Exception as e:
        
            print(f"❌ Error leyendo {ruta_archivo}: {e}")
            
    return textos

# ============================================================
# PROCESAR ARCHIVO → TRADUCIR y GUARDAR TMP + FINAL
# ============================================================
def procesar_archivo_traducciones(ruta_archivo, diccionario, idioma_destino='es'):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido_original = f.read()

        contenido_traducido = contenido_original
        textos_unicos = list(set(extraer_textos_archivo(ruta_archivo)))

        for texto in textos_unicos:
            if "show()" in texto:
                continue
            traduccion = traducir_por_texto(texto, diccionario, idioma_destino)
            if traduccion and texto != traduccion:
                contenido_traducido = contenido_traducido.replace(texto, traduccion)

        nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]

        # TMP con prefijo de idioma
        ruta_tmp = os.path.join(TMP_DIR, f"{idioma_destino}_{nombre_base}.py")
        with open(ruta_tmp, 'w', encoding='utf-8') as f:
            f.write(contenido_traducido)

        return ruta_tmp
    except Exception as e:
        print(f"❌ Error procesando {ruta_archivo}: {e}")
        return None

# ============================================================
# OBTENER IDIOMAS
# ============================================================
def obtener_idiomas_disponibles(diccionario):
    idiomas = set()
    for info in diccionario.values():
        idiomas.update(info['traducciones'].keys())
    return sorted(idiomas)

# ============================================================
# MAIN
# ============================================================
def main():
    print("🚀 EXPLORAR.PY — SISTEMA POR TEXTO")
    print("=" * 50)

    diccionario = cargar_diccionario_por_texto()
    if not diccionario:
        print("❌ No se pudo cargar el diccionario.")
        return

    idiomas_disponibles = obtener_idiomas_disponibles(diccionario)
    print("\n🌍 Idiomas disponibles:", idiomas_disponibles)

    idioma_destino = input("👉 Idioma destino (enter = en): ").strip().lower()
    if not idioma_destino:
        idioma_destino = "en"

    print("\n🔄 Buscando archivos...")

    archivos_py = glob.glob(os.path.join(BASE, "*.py"))
    archivos_procesados = 0
    archivos_generados = []

    for archivo in archivos_py:
        nombre = os.path.basename(archivo).lower()
        if "explorar" in nombre or "diccionario" in nombre:
            continue

        ruta_final = procesar_archivo_traducciones(archivo, diccionario, idioma_destino)
        if ruta_final:
            archivos_generados.append(ruta_final)
            archivos_procesados += 1

    print("\n🎯 Archivos traducidos generados:", archivos_procesados)

    # ============================================================
    # Ejecutar cada script traducido en subproceso
    # ============================================================
    print("\n🔄 Ejecutando scripts traducidos para generar gráficas...")
    for script in archivos_generados:
        try:
            subprocess.run(['python', script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error ejecutando {script}: {e}")

    print("\n✅ COMPLETADO")
    print(f"🌍 Idioma destino: {idioma_destino}")


if __name__ == "__main__":
    main()
