#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para generar diccionarios de traducción a partir de global.csv
usando el español como referencia absoluta.

Uso:
    python3 busca-regenera.py
    python3 busca-regenera.py --help

Reglas:
- El español (es-*.dic) es la referencia.
- El campo archivo SIEMPRE contiene programa.py.
- Los archivos físicos .dic NUNCA llevan .py.
- No se borra nada mientras se lee.
- Solo se escribe un diccionario si:
    - existe el español correspondiente
    - hay al menos una línea válida
- El texto (4º campo) NUNCA se modifica.
- Se hace trim SOLO en idioma, archivo y id.
"""

import csv
from pathlib import Path
import io
import sys
import subprocess

# =====================================
# Rutas
# =====================================
BASE_DIR = Path(__file__).parent.resolve()
DIC_DIR = BASE_DIR.parent / "dic"
GLOBAL_CSV = DIC_DIR / "global.csv"

DIC_DIR.mkdir(exist_ok=True)

# =====================================
# Cargar diccionarios españoles
# =====================================
def cargar_diccionario_es():
    dic_es = {}
    for ruta in DIC_DIR.glob("es-*.dic"):
        with ruta.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for fila in reader:
                if len(fila) < 4:
                    continue
                archivo = fila[1].strip()   # programa.py
                id_linea = fila[2].strip()
                texto = fila[3]            # NO tocar
                dic_es.setdefault(archivo, {})[id_linea] = texto
    return dic_es

# =====================================
# Abrir CSV con detección de codificación
# =====================================
def abrir_csv(path):
    raw = path.read_bytes()
    if raw.startswith((b'\xff\xfe', b'\xfe\xff')):
        encoding = "utf-16"
    else:
        encoding = "utf-8-sig"
    return io.StringIO(raw.decode(encoding))

# =====================================
# Main
# =====================================
def main():

    if "--help" in sys.argv:
        print(__doc__)
        return

    if not GLOBAL_CSV.exists():
        print("❌ No se encuentra global.csv")

    # Español como referencia
    dic_es = cargar_diccionario_es()

    # Diccionarios en memoria
    dic_idiomas = {}

    # ---------------------------------
    # Leer global.csv COMPLETO
    # ---------------------------------
    with abrir_csv(GLOBAL_CSV) as f:
        reader = csv.reader(f, delimiter=";", quoting=csv.QUOTE_NONE)
        next(reader, None)

        for fila in reader:
            if len(fila) < 4:
                continue

            idioma  = fila[0].strip().lower()
            archivo = fila[1].strip()   # programa.py
            id_linea = fila[2].strip()
            texto   = fila[3]           # NO tocar

            if idioma == "es":
                continue

            dic_idiomas \
                .setdefault(idioma, {}) \
                .setdefault(archivo, {})[id_linea] = texto

    # ---------------------------------
    # Guardado FINAL
    # ---------------------------------
    for idioma, archivos in dic_idiomas.items():
        for archivo, lineas in archivos.items():

            if archivo not in dic_es:
                continue

            if not lineas:
                continue

            archivo_fisico = archivo.replace(".py", "")
            ruta = DIC_DIR / f"{idioma}-{archivo_fisico}.dic"

            with ruta.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["idioma", "archivo", "id", "texto"])
                for id_linea, texto in lineas.items():
                    writer.writerow([idioma, archivo, id_linea, texto])

    # ---------------------------------
    # TEST FINAL
    # ---------------------------------
    print("\n===== Estadísticas finales =====")
    print("OK  IDI  ES    Diccionario")

    # recorrer todos los es-*.dic
    for ruta_es in sorted(DIC_DIR.glob("es-*.dic")):
        programa_py = ruta_es.name[3:-4] + ".py"  # quitar "es-" y ".dic"
        
        # contar líneas del español
        with ruta_es.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            total_es = sum(1 for _ in reader)

        # para cada diccionario de otros idiomas que corresponda a este español
        for ruta_idioma in sorted(DIC_DIR.glob(f"*-{programa_py.replace('.py','')}.dic")):
            nombre = ruta_idioma.name
            if nombre.startswith("es-"):
                continue

            # contar líneas del idioma
            with ruta_idioma.open("r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f, delimiter=";")
                next(reader, None)
                total_idioma = sum(1 for _ in reader)

            icono = "✅" if total_idioma == total_es else "❌"
            print(f"{icono} {total_idioma:<4} {total_es:<4} {nombre}")
        
        print("\n")

    # ---------------------------------
    # TEST FINAL
    # ---------------------------------
    print("\n===== Estadísticas finales =====")
    print("OK  IDI  ES    Diccionario")

    diccionarios_detectados = set()

    # recorrer todos los es-*.dic
    for ruta_es in sorted(DIC_DIR.glob("es-*.dic")):
        programa_py = ruta_es.name[3:-4] + ".py"  # quitar "es-" y ".dic"
        diccionario = ruta_es.name[3:-4]          # nombre base del diccionario
        
        # contar líneas del español
        with ruta_es.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            total_es = sum(1 for _ in reader)

        # para cada diccionario de otros idiomas que corresponda a este español
        for ruta_idioma in sorted(DIC_DIR.glob(f"*-{diccionario}.dic")):
            nombre = ruta_idioma.name
            if nombre.startswith("es-"):
                continue

            idioma = nombre.split("-", 1)[0]
            diccionarios_detectados.add(diccionario)

            # contar líneas del idioma
            with ruta_idioma.open("r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f, delimiter=";")
                next(reader, None)
                total_idioma = sum(1 for _ in reader)

            icono = "✅" if total_idioma == total_es else "❌"
            print(f"{icono} {total_idioma:<4} {total_es:<4} {nombre}")

        print("\n")

    # ---------------------------------
    # PREGUNTA FINAL PARA GRÁFICAS
    # ---------------------------------
    if diccionarios_detectados:
        resp = input("¿Deseas generar también las gráficas para todos los diccionarios? [s/N]: ").strip().lower()

        if resp in ("s", "si", "sí", "y", "yes"):
            print("\n📊 Generando gráficas...\n")
            for diccionario in sorted(diccionarios_detectados):
                subprocess.run(["python", "explorar.py", f"{diccionario}.py", "todos"])
                print(f"python explorar.py {diccionario}  todos")

# =====================================
if __name__ == "__main__":
    main()
