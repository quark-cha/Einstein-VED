#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from pathlib import Path

# =====================================
# Directorios base
# =====================================
BASE_DIR = Path(__file__).parent.resolve()
DIC_DIR = BASE_DIR.parent / "dic"
GLOBAL_CSV = DIC_DIR / "global.csv"

DIC_DIR.mkdir(exist_ok=True)

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

# =====================================
# Guardar diccionario de idioma a disco
# =====================================
def guardar_diccionario(idioma, diccionario):
    for archivo, lineas in diccionario.items():
        archivo_sinpy = archivo.replace(".py", "")
        ruta = DIC_DIR / f"{idioma}-{archivo_sinpy}.dic"
        with ruta.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["idioma", "archivo", "id", "texto"])
            for id_linea, texto in lineas.items():
                writer.writerow([idioma, archivo, id_linea, texto])

# =====================================
# Main
# =====================================
def main():
    if not GLOBAL_CSV.exists():
        print(f"❌ No se encuentra {GLOBAL_CSV}")
        return

    # Cargar diccionarios en memoria
    dic_es = cargar_diccionario_espanol()
    dic_idiomas = cargar_diccionarios_idiomas()

    idiomas_en_csv = set()

    # Procesar global.csv línea por línea
    with GLOBAL_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter=";", quoting=csv.QUOTE_NONE)
        next(reader, None)  # saltar cabecera si existe
        cuenta_lineas = 0
        for fila in reader:
            cuenta_lineas += 1
            if len(fila) < 4:
                continue
            idioma = fila[0].strip().lower()
            archivo = fila[1].strip()
            id_linea = fila[2].strip()
            texto = fila[3]

            if idioma == "es":
                continue  # español es referencia absoluta

            # Inicializar diccionario en memoria si no existe
            if idioma not in dic_idiomas:
                dic_idiomas[idioma] = {}
            if archivo not in dic_idiomas[idioma]:
                dic_idiomas[idioma][archivo] = {}

            # Añadir solo si no existe ya
            if id_linea not in dic_idiomas[idioma][archivo]:
                dic_idiomas[idioma][archivo][id_linea] = texto
                
            idiomas_en_csv.add(idioma)
            print(f"\rProcesando línea: {cuenta_lineas}", end="", flush=True)
        
        print("",flush=False)  # salto de línea final

    print("\n\n===== Guardando diccionarios actualizados =====")
    # Guardar diccionarios actualizados
    for idioma, dic in dic_idiomas.items():
        guardar_diccionario(idioma, dic)

    # Estadísticas
    print("\n===== Estadísticas finales =====")
    for idioma, archivos in dic_idiomas.items():
        for archivo, lineas in archivos.items():
            archivo_sinpy = archivo.replace(".py", ".dic")
            total_es = len(dic_es.get(archivo, {}))
            total_idioma = len(lineas)
            test = "❌"
            if total_idioma == total_es:
                test = "✅"
            print(f"{test} {total_idioma:<4} {total_es:<5} {idioma:>8}-{archivo}")
    print("Procesado completado para idiomas:", ", ".join(sorted(idiomas_en_csv)))

if __name__ == "__main__":
    main()
