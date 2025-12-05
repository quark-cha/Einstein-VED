# 1-init-dic.py
#
# 
# Script que crea un diccionario en español a partir de archivos .py de gráficas.
# Escanea todos los textos en español dentro del código y genera un archivo
# ..\dic\es-<archivo>.dic que servirá como base para traducciones a otros idiomas.
# 
# ----------------------------------------------------------------------
# 
# Uso:
# python 1-init-dic.py [archivo.py|todos]
# 
# Argumentos:
# archivo.py -> Archivo Python del que se generará el diccionario.
#               Si no se proporciona, el script pedirá la ruta y explicará qué hace.
# "todos"     -> Procesa todos los archivos .py en ../src
# ----------------------------------------------------------------------
# 
# Requisitos:
# - Python 3.x
# - Permisos de escritura en ..\dic\
# ----------------------------------------------------------------------
# 
# Este script se ejecuta como clase InitDic que gestiona:
# - Escaneo de archivos
# - Extracción de cadenas de texto en español
# - Generación del diccionario ..\dic\es-<archivo>.dic
# 
# ----------------------------------------------------------------------

import os
import sys
import glob
import re

class InitDic:
    def __init__(self, archivo=None):
        self.archivo = archivo
        self.directorio_src = os.path.join("..", "src")
        self.directorio_dic = os.path.join("..", "dic")
        if not os.path.exists(self.directorio_dic):
            os.makedirs(self.directorio_dic)
        # Palabras y patrones a excluir
        self.palabras_excluidas = set([
            "bold", "top", "bottom", "red", "of", "on", "center", "green", 
            "enter", "equal", "right", "svg", "png", "jpeg", "blue", "orange",
            "left", "save", "load", "file", "edit", "view", "help", "tools",
            "settings", "options", "window", "menu", "button", "label", "text",
            "input", "output", "data", "plot", "chart", "graph", "axis", "title",
            "legend", "grid", "color", "size", "width", "height", "margin",
            "padding", "border", "background", "font", "style", "class", "id",
            "function", "method", "variable", "constant", "parameter", "return",
            "import", "export", "module", "package", "library", "framework",
            "database", "server", "client", "network", "protocol", "api",
            "json", "xml", "html", "css", "javascript", "python", "java",
            "c++", "c#", "php", "ruby", "sql", "nosql", "mysql", "postgresql",
            "mongodb", "redis", "docker", "kubernetes", "aws", "azure", "gcp"
        ])

    def crear_diccionario(self):
        archivos_a_procesar = []

        if not self.archivo:
            print("🔹 Este script genera diccionarios en español a partir de archivos .py en ../src")
            print("Uso: python 1-init-dic.py [archivo.py|todos]")
            return

        if self.archivo.lower() == "todos":
            archivos_a_procesar = glob.glob(os.path.join(self.directorio_src, "*.py"))
        else:
            archivo_path = os.path.join(self.directorio_src, self.archivo)
            if not os.path.exists(archivo_path):
                print(f"❌ Archivo {archivo_path} no encontrado")
                return
            archivos_a_procesar = [archivo_path]

        if not archivos_a_procesar:
            print("❌ No se encontraron archivos a procesar")
            return

        for archivo in archivos_a_procesar:
            textos = self.extraer_textos_espanol_con_lineas(archivo)
            if not textos:
                print(f"❌ No se encontraron textos en {archivo}")
                continue

            nombre_base = os.path.basename(archivo).replace(".py","")
            archivo_dic = os.path.join(self.directorio_dic, f"es-{nombre_base}.dic")
            
            with open(archivo_dic, 'w', encoding='utf-8') as f:
                f.write("idioma;archivo;id;texto_traducido\n")
                for t in textos:
                    f.write(f"es;{t['archivo']};{t['id']};{t['texto']}\n")
            
            print(f"✅ Diccionario generado: {archivo_dic}")
            print(f"📝 Total entradas: {len(textos)}")

    def extraer_textos_espanol_con_lineas(self, ruta_archivo):
        textos = []
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
            nombre_archivo = os.path.basename(ruta_archivo)
            
            for num_linea, linea in enumerate(lineas, 1):
                for comilla in ('"', "'"):
                    i = 0
                    while i < len(linea):
                        if linea[i] == comilla:
                            start = i + 1
                            i += 1
                            while i < len(linea) and linea[i] != comilla:
                                i += 1
                            if i < len(linea):
                                texto = linea[start:i].strip()
                                if self._es_texto_valido(texto):
                                    id_texto = f"{num_linea:04d}"
                                    textos.append({
                                        'archivo': nombre_archivo,
                                        'id': id_texto,
                                        'texto': texto
                                    })
                                i += 1
                        else:
                            i += 1
        except Exception as e:
            print(f"❌ Error extrayendo textos de {ruta_archivo}: {e}")
        return textos

    def _es_texto_valido(self, texto):
        if not texto or len(texto) < 3:
            return False
        if texto.lower() in self.palabras_excluidas:
            return False
        if re.match(r'^#', texto):
            return False
        # Evitar extensiones de archivo
        if any(ext in texto.lower() for ext in (".png",".jpg",".jpeg",".svg",".gif",".pdf",".eps")):
            return False
        # Evitar que sea solo números
        if texto.replace(".","").replace(",","").replace(" ","").isdigit():
            return False
        # Evitar colores hex
        if re.match(r'^#[0-9A-Fa-f]{3,8}$', texto):
            return False
        # Evitar cadenas demasiado técnicas o nombres de variables
        if re.match(r'^[a-zA-Z0-9_]+$', texto):
            return False
        return True

def main():
    archivo = sys.argv[1] if len(sys.argv) > 1 else None
    init_dic = InitDic(archivo)
    init_dic.crear_diccionario()

if __name__ == "__main__":
    main()
