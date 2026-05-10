import os
import re
import sys

# Configuración
DIR_SRC = "../src"
DIR_TMP = "../tmp"
DIR_IMG = "../img"
IDIOMAS = ["ar","ch","de","en","fr","it","sk"]

def extraer_imagenes(py_path):
    """Busca patrones de nombres de imágenes dentro del .py"""
    imagenes = set()
    if not os.path.isfile(py_path):
        return imagenes
    with open(py_path,"r",encoding="utf-8") as f:
        for line in f:
            # Busca .png, .svg, .jpg entre comillas o con prefijo
            matches = re.findall(r"['\"]([a-zA-Z0-9_\-]+?\.(?:png|svg|jpg))['\"]", line)
            imagenes.update(matches)
    return imagenes

def generar_tabla(modo="normal"):
    tabla = []
    if modo=="normal":
        directorio = DIR_SRC
    else:  # todos
        directorio = DIR_TMP

    for f in sorted(os.listdir(directorio)):
        if not f.endswith(".py"):
            continue
        py_base = f
        py_path = os.path.join(directorio, f)
        imagenes = extraer_imagenes(py_path)
        if modo=="todos":
            py_base = re.sub(r"^[a-z]{2}_","",py_base)  # quitar prefijo idioma
        for img in imagenes:
            existencia = ""
            if modo=="normal":
                for idioma in IDIOMAS:
                    img_pref = f"{idioma}_{img}"
                    if os.path.isfile(os.path.join(DIR_IMG,img_pref)):
                        existencia += f" {idioma}✅"
            else:  # en modo todos
                idiomas_existentes = [idioma for idioma in IDIOMAS
                                      if os.path.isfile(os.path.join(DIR_IMG,f"{idioma}_{img}"))]
                if idiomas_existentes:
                    existencia = " ".join(f"{i}✅" for i in idiomas_existentes)
                else:
                    existencia = "❌"
            tabla.append((py_base,img,existencia))
    return tabla

def imprimir_tabla(tabla):
    # Calcular ancho de la columna izquierda
    ancho_izq = max(len(row[0]) for row in tabla) + 2
    ancho_med = max(len(row[1]) for row in tabla) + 2
    print("-"*(ancho_izq + ancho_med + 10))
    for row in tabla:
        print(f"{row[0].ljust(ancho_izq)}| {row[1].ljust(ancho_med)}| {row[2]}")
    print("-"*(ancho_izq + ancho_med + 10))

if __name__=="__main__":
    modo = "normal"
    if len(sys.argv)>1 and sys.argv[1].lower() in ["todos","todo"]:
        modo = "todos"
    tabla = generar_tabla(modo)
    imprimir_tabla(tabla)
