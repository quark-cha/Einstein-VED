import os
import csv
import glob

# ======================================
# RUTAS BASE
# ======================================
BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_DICCIONARIO = os.path.join(BASE, "diccionario.csv")

# ======================================
# LEER ARCHIVOS PYTHON
# ======================================
def extraer_textos_archivo(ruta_archivo):
    textos = []
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()

        # Extrae "..." y '...'
        for comilla in ['"', "'"]:
            i = 0
            while i < len(contenido):
                if contenido[i] == comilla:
                    inicio = i + 1
                    i += 1
                    while i < len(contenido) and contenido[i] != comilla:
                        i += 1
                    if i < len(contenido):
                        texto = contenido[inicio:i].strip()
                        # no guardar basura
                        if len(texto) >= 3 and any(c.isalpha() for c in texto):
                            textos.append(texto)
                        i += 1
                else:
                    i += 1
    except Exception as e:
        print(f"❌ Error leyendo {ruta_archivo}: {e}")

    return textos

# ======================================
# CARGAR DICCIONARIO EXISTENTE
# ======================================
def cargar_diccionario_existente():
    dic = {}  # clave = (archivo, id) → info

    if not os.path.exists(RUTA_DICCIONARIO):
        print("⚠️ No existe diccionario.csv, se creará uno nuevo.")
        return dic

    try:
        with open(RUTA_DICCIONARIO, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)

            for fila in reader:
                if len(fila) < 4:
                    continue
                idioma, archivo, id_texto, texto = fila
                clave = (archivo, id_texto)

                if clave not in dic:
                    dic[clave] = {"es": "", "traducciones": {}}

                if idioma == "es":
                    dic[clave]["es"] = texto
                else:
                    dic[clave]["traducciones"][idioma] = texto
    except Exception as e:
        print("❌ Error leyendo diccionario existente:", e)

    return dic

# ======================================
# GUARDAR DICCIONARIO
# ======================================
def guardar_diccionario(diccionario):
    try:
        with open(RUTA_DICCIONARIO, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["idioma", "archivo", "id", "texto"])

            for (archivo, id_texto), info in diccionario.items():
                writer.writerow(["es", archivo, id_texto, info["es"]])
                for idioma, texto in info["traducciones"].items():
                    writer.writerow([idioma, archivo, id_texto, texto])

        print("💾 Diccionario actualizado correctamente.")
    except Exception as e:
        print("❌ Error guardando diccionario:", e)

# ======================================
# CREAR NUEVAS ENTRADAS ESPAÑOL
# ======================================
def generar_diccionario():
    print("🔎 Escaneando scripts para extraer textos...")

    diccionario = cargar_diccionario_existente()
    archivos = glob.glob(os.path.join(BASE, "*.py"))

    total_nuevos = 0

    for ruta in archivos:
        nombre = os.path.basename(ruta)
        if "explorar" in nombre.lower() or "diccionario" in nombre.lower():
            continue  # no tocar estos

        textos = extraer_textos_archivo(ruta)

        id_linea = 1
        for texto in textos:
            clave = (nombre, str(id_linea))

            # Si ya existe, no lo pisamos
            if clave not in diccionario:
                diccionario[clave] = {
                    "es": texto,
                    "traducciones": {}
                }
                total_nuevos += 1

            id_linea += 1

    print(f"📝 Nuevos textos añadidos: {total_nuevos}")
    guardar_diccionario(diccionario)

# ======================================
# MAIN
# ======================================
if __name__ == "__main__":
    print("🚀 Generador/actualizador de diccionario")
    generar_diccionario()
