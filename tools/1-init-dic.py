"""
1-init-dic.py - Extractor Avanzado de Diccionarios y Detector de Gráficas
==========================================================================
Versión: 2.0 Avanzada
Autor: Sistema VED
Descripción: Extrae textos para traducción y detecta gráficas generadas
"""

import os
import sys
import glob
import re
import json
from datetime import datetime
from collections import defaultdict
import tokenize
from io import BytesIO
import csv

NO_TRADUCIR = [
    "\\n", "\\r", "dejavu sans", "dejavu sans mono", "arial", "times new roman",
    "matplotlib", "plotly", "seaborn", 
    "agg", "blue", "green", "red", "black", "white", "yellow",
    "gray", "grey", "cyan", "magenta", "purple", "orange",
    "tight", "normal", "bold", "dashed", "round",
    "on", "off", "log", "linear", "equal", "auto",
    "anchor", "default", "best",
    "upper", "lower", "center", "left", "right",
    "polar", "rectilinear", "3d",
    "symlog", "logit",
    "top", "bottom", "both",
    "box", "title", "label", "xlabel", "ylabel", "zlabel",
    "size", "width", "height", "color", "font", "fontsize",
    "fig", "ax", "axes", "plt", "show", "plot", "scatter",
    "bar", "hist", "pie", "boxplot", "contour", "imshow",
    "x", "y", "z", "w", "h", "d", "r", "g", "b", "alpha",
    "true", "false", "none", "nan", "inf",
    "sans-serif", "lightblue", "lightgreen", "lightgrey",
    "darkblue", "darkgreen", "darkred",
    "axes.unicode_minus", "font.sans-serif", "font.family",
    "liberation sans", "__main__"
]


def contiene_palabra_espanola(texto: str) -> bool:
    """Verifica si un texto contiene palabras en español con vocales y consonantes"""
    palabras = re.findall(r"[A-Za-zÁÉÍÓÚÜáéíóúüÑñ]+", texto)
    
    for p in palabras:
        if len(p) <= 3:
            continue
        if re.search(r"[aeiouáéíóúüAEIOUÁÉÍÓÚÜ]", p) and \
           re.search(r"[bcdfghjklmnñpqrstvwxyzBCDFGHJKLMNÑPQRSTVWXYZ]", p):
            return True
    return False

# MÉTODO INFALIBLE: Procesar carácter por carácter
def encontrar_cadenas_manual(texto):
    """Método manual que SÍ funciona"""
    cadenas = []
    i = 0
    n = len(texto)
    
    while i < n:
        # Si encontramos un prefijo de cadena
        if texto[i] in 'bruf' and i+1 < n and texto[i+1] in '"\'':  # Prefijos
            inicio = i
            i += 1
        elif texto[i] in '"\'':  # Comilla normal
            inicio = i
        else:
            i += 1
            continue
        
        # Determinar tipo de comilla
        comilla = texto[i]
        i += 1
        
        # Verificar si es triple comilla
        es_triple = False
        if i+1 < n and texto[i] == comilla and texto[i+1] == comilla:
            es_triple = True
            i += 2  # Saltar las otras dos comillas
        
        # Buscar el cierre
        while i < n:
            if texto[i] == '\\':  # Escape, saltar siguiente carácter
                i += 2
                continue
            
            if not es_triple:
                if texto[i] == comilla:  # Cierre de cadena simple
                    i += 1
                    cadenas.append(texto[inicio:i])
                    break
            else:
                # Para triple comilla, buscar tres seguidas
                if texto[i] == comilla and i+2 < n and texto[i+1] == comilla and texto[i+2] == comilla:
                    i += 3
                    cadenas.append(texto[inicio:i])
                    break
            
            i += 1
    
    return cadenas


class DiccionarioGraficas:
    def __init__(self, archivo=None):
        self.archivo = archivo
        
        # Rutas absolutas para evitar problemas
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.DIC_DIR = os.path.join(script_dir, "..", "dic")
        self.SRC_DIR = os.path.join(script_dir, "..", "src")
        
        # Archivos reservados (no se modifican) - SOLO .dic
        self.reservados = ["es-base.dic", "es-plantilla.dic"]
        
        # Estadísticas y resumen
        self.resumen = {
            'inicio': datetime.now(),
            'total_archivos': 0,
            'procesados': 0,
            'omitidos': 0,
            'diccionarios': defaultdict(dict),
            'graficas': defaultdict(list),
            'errores': []
        }
        
        # Patrones para detectar gráficas - SOLO LOS QUE GENERAN FICHEROS
        self.patrones_graficas = [
            # Guardado de archivos (SOLO ESTOS INTERESAN)
            (r'savefig\([^)]*[\'"]([^\'"]+\.(?:png|svg|jpg|jpeg|pdf|eps|tiff|bmp|gif))[\'"]', 'savefig'),
            (r'\.savefig\([^)]*[\'"]([^\'"]+\.(?:png|svg|jpg|jpeg|pdf|eps|tiff|bmp|gif))[\'"]', 'savefig'),
            (r'write_image\([^)]*[\'"]([^\'"]+\.(?:png|svg|jpg|jpeg|pdf))[\'"]', 'write_image'),
            (r'save\([^)]*[\'"]([^\'"]+\.(?:png|svg|jpg|jpeg|pdf))[\'"]', 'save'),
            # También capturar fig.savefig()
            (r'fig\.savefig\([^)]*[\'"]([^\'"]+\.(?:png|svg|jpg|jpeg|pdf|eps))[\'"]', 'savefig'),
            (r'ax\.figure\.savefig\([^)]*[\'"]([^\'"]+\.(?:png|svg|jpg|jpeg|pdf))[\'"]', 'savefig'),
        ]
        
        # Encabezado
        self._mostrar_encabezado()

    def _procesar_archivo(self, archivo_src):
        """Procesa un archivo individual"""
        nombre_base = os.path.basename(archivo_src)
        nombre_sin_ext = os.path.splitext(nombre_base)[0]
        
        print(f"\n{'='*60}")
        print(f"📄 PROCESANDO: {nombre_base}")
        print(f"{'='*60}")
        
        # Detectar gráficas
        graficas = self._detectar_graficas(archivo_src)
        self.resumen['graficas'][nombre_base] = graficas
        
        # Extraer textos
        textos = self._extraer_textos(archivo_src)
        
        if textos:
            print(f"\n🔤 TEXTOS PARA TRADUCCIÓN ({len(textos)}):")
            for i, t in enumerate(textos[:3], 1):
                texto_trunc = t['texto'][:60] + ('...' if len(t['texto']) > 60 else '')
                print(f"   {i}. Línea {t['linea']:4d}: \"{texto_trunc}\"")
            if len(textos) > 3:
                print(f"       ... y {len(textos) - 3} más")
        else:
            print(f"\nℹ️  No se encontraron textos para extraer")
        
        # Crear diccionario si hay textos
        if textos:
            exito = self._crear_diccionario(archivo_src, textos, graficas)
            if exito:
                print(f"\n✅ DICCIONARIO CREADO:")
                print(f"   • es-{nombre_sin_ext}.dic")
                print(f"   • {len(textos)} textos | {len(graficas)} gráficas detectadas")
                self.resumen['procesados'] += 1
            else:
                print(f"\n❌ ERROR creando diccionario")
        else:
            print(f"\n⚠️  No se creó diccionario (sin textos)")
            self.resumen['omitidos'] += 1


    def ejecutar(self):
        """Método principal de ejecución"""
        
        # Verificar directorios
        if not self._verificar_directorios():
            return
        
        # Determinar qué archivos procesar
        archivos_src = sorted(glob.glob(os.path.join(self.SRC_DIR, "*.py")))
        
        if not self.archivo or self.archivo.lower() == "todos":
            archivos_a_procesar = archivos_src
            print(f"\n🎯 PROCESANDO TODOS LOS ARCHIVOS ({len(archivos_a_procesar)})")
        else:
            # Buscar archivo específico
            archivos_a_procesar = []
            for archivo in archivos_src:
                if os.path.basename(archivo) == self.archivo:
                    archivos_a_procesar.append(archivo)
                    break
            
            if not archivos_a_procesar:
                print(f"\n❌ ERROR: Archivo '{self.archivo}' no encontrado")
                print(f"   Archivos disponibles en src/:")
                for archivo in archivos_src[:15]:
                    print(f"   • {os.path.basename(archivo)}")
                return
        
        # Procesar cada archivo
        for archivo in archivos_a_procesar:
            self._procesar_archivo(archivo)
        
        # Mostrar resumen final
        self._mostrar_resumen_final()

    # ------------------------------------------------------------
    
    def _mostrar_encabezado(self):
        """Muestra el encabezado del programa"""
        print("\n" + "="*80)
        print(" " * 20 + "📊 GESTOR AVANZADO DE DICCIONARIOS VED")
        print("="*80)
        print("   Versión: 2.0 Avanzada - Detector de Gráficas Integrado")
        print("   Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("="*80)
        
        # Mostrar rutas
        print(f"\n📁 DIRECTORIOS:")
        print(f"   • Fuente:    {self.SRC_DIR}")
        print(f"   • Diccionarios: {self.DIC_DIR}")
        print(f"   • Reservados: {', '.join(self.reservados)}")
        
    # ------------------------------------------------------------
    
    def _verificar_directorios(self):
        """Verifica y prepara los directorios necesarios"""
        print(f"\n🔍 VERIFICANDO ESTRUCTURA...")
        
        # Verificar directorio src
        if not os.path.exists(self.SRC_DIR):
            print(f"❌ ERROR: No existe directorio SRC: {self.SRC_DIR}")
            print(f"   Creando estructura...")
            os.makedirs(self.SRC_DIR, exist_ok=True)
            print(f"   ✅ Directorio SRC creado")
            return False
        
        # Verificar directorio dic
        if not os.path.exists(self.DIC_DIR):
            print(f"📁 Creando directorio DIC: {self.DIC_DIR}")
            os.makedirs(self.DIC_DIR, exist_ok=True)
            print(f"   ✅ Directorio DIC creado")
        
        # Mostrar contenido
        archivos_src = glob.glob(os.path.join(self.SRC_DIR, "*.py"))
        self.resumen['total_archivos'] = len(archivos_src)
        
        if archivos_src:
            print(f"\n📄 ARCHIVOS ENCONTRADOS EN SRC/ ({len(archivos_src)}):")
            for i, archivo in enumerate(sorted(archivos_src)[:10], 1):
                nombre = os.path.basename(archivo)
                tamaño = os.path.getsize(archivo)
                print(f"   {i:2d}. {nombre:30s} ({tamaño:,} bytes)")
            if len(archivos_src) > 10:
                print(f"   ... y {len(archivos_src) - 10} más")
        else:
            print(f"\n⚠️  ADVERTENCIA: No hay archivos .py en {self.SRC_DIR}")
            print(f"   Coloca tus scripts de gráficas en esa carpeta")
            return False
            
        return True
    
    # ------------------------------------------------------------
    
    def _detectar_graficas(self, ruta_archivo):
        """Analiza un archivo .py para detectar gráficas generadas - SOLO FICHEROS"""
        graficas = []
        nombre_archivo = os.path.basename(ruta_archivo)
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
                lineas = contenido.split('\n')
            
            # Buscar en cada línea
            for num_linea, linea in enumerate(lineas, 1):
                linea_limpia = linea.strip()
                
                # Saltar comentarios y líneas vacías
                if not linea_limpia or linea_limpia.startswith('#'):
                    continue
                
                # Buscar patrones de gráficas - SOLO LOS QUE GENERAN FICHEROS
                for patron, tipo in self.patrones_graficas:
                    matches = re.finditer(patron, linea, re.IGNORECASE)
                    for match in matches:
                        # SOLO nos interesan los que generan ficheros
                        if tipo in ['savefig', 'write_image', 'save']:
                            # Extraer nombre de archivo
                            nombre_grafica = match.group(1) if match.groups() else f"grafica_linea_{num_linea}"
                            extension = nombre_grafica.split('.')[-1] if '.' in nombre_grafica else 'png'
                            
                            graficas.append({
                                'tipo': tipo,
                                'nombre': nombre_grafica,
                                'extension': extension,
                                'linea': num_linea,
                                'codigo': linea_limpia[:60] + ('...' if len(linea_limpia) > 60 else '')
                            })
            
            # Eliminar duplicados
            graficas_unicas = []
            vistas = set()
            for g in graficas:
                clave = (g['nombre'], g['linea'])
                if clave not in vistas:
                    vistas.add(clave)
                    graficas_unicas.append(g)
            
            # Ordenar por línea
            graficas_unicas.sort(key=lambda x: x['linea'])
            
            return graficas_unicas
            
        except Exception as e:
            error_msg = f"Error analizando {nombre_archivo}: {str(e)}"
            self.resumen['errores'].append(error_msg)
            return []
    
    # ------------------------------------------------------------
    
    def _extraer_textos(self, ruta_archivo):
        """Extrae textos para traducción de un archivo .py usando tokenize"""
        textos = []

        try:
            with open(ruta_archivo, 'rb') as f:  # abrir en modo bytes
                tokens = tokenize.tokenize(f.readline)
                for toknum, tokval, start, end, line in tokens:
                    if toknum == tokenize.STRING:
                        # tokval contiene la cadena literal, start[0] es el número de línea
                        try:
                            texto_valor = eval(tokval)
                        except Exception:
                            continue  # Saltar cadenas mal formateadas

                        # Filtrado NO_TRADUCIR y mínimo 4 caracteres
                        if not texto_valor or len(texto_valor) <= 4:
                            continue
                        if texto_valor.lower() in NO_TRADUCIR:
                            continue
                        if texto_valor.lower().endswith(('.png', '.svg', '.jpg', '.jpeg', '.pdf', '.eps', '.tiff', '.bmp', '.gif')):
                            continue  # NO incluir nombres de archivos de gráficas
                        if bool(re.fullmatch(r'#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})', texto_valor)):
                            continue  # NO incluir códigos de color hexadecimales

                        # Guardar texto válido
                        textos.append({
                            'linea': start[0],
                            'texto': texto_valor,
                            'contexto': line.strip()[:80]
                        })

            return textos

        except Exception as e:
            self.resumen['errores'].append(f"Error extrayendo textos de {ruta_archivo}: {str(e)}")
            return []
        # ------------------------------------------------------------
    
    def _crear_diccionario(self, archivo_src, textos, graficas):
        nombre_base = os.path.basename(archivo_src)
        nombre_sin_ext = os.path.splitext(nombre_base)[0]

        # Evitar sobrescribir archivos reservados
        nombre_dic = f"es-{nombre_sin_ext}.dic"
        if nombre_dic in self.reservados:
            print(f"\n🛡️  ARCHIVO RESERVADO: {nombre_dic}")
            self.resumen['omitidos'] += 1
            return False

        ruta_dic = os.path.join(self.DIC_DIR, nombre_dic)

        if os.path.exists(ruta_dic):
            respuesta = input(f"\n⚠️  El archivo {nombre_dic} YA EXISTE. ¿Sobrescribir? (s/N): ").strip().lower()
            if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
                print("   ✅ Conservando archivo existente.")
                return False

        try:
            with open(ruta_dic, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONE, escapechar='\\')
                writer.writerow(['idioma', 'archivo', 'linea', 'texto_traducido'])

                for t in textos:
                    texto = t['texto'].replace('\r\n', '\n').replace('\n', '\\n').strip()

                    # Filtrar textos muy cortos
                    if len(texto) <= 4:
                        continue

                    writer.writerow(['es', nombre_base, t['linea'], texto])

            # Actualizar resumen
            self.resumen['diccionarios'][nombre_base] = {
                'archivo_dic': ruta_dic,
                'textos': len(textos),
                'graficas': len(graficas)
            }

            return True

        except Exception as e:
            error_msg = f"Error guardando diccionario {nombre_dic}: {str(e)}"
            self.resumen['errores'].append(error_msg)
            return False
    
    def _mostrar_resumen_final(self):
        """Muestra el resumen completo al final - SOLO FICHEROS DE GRÁFICAS"""
        duracion = datetime.now() - self.resumen['inicio']
        
        print(f"\n{'='*80}")
        print(" " * 25 + "📋 RESUMEN FINAL DEL PROCESO")
        print(f"{'='*80}")
        
        print(f"\n⏱️  TIEMPO TOTAL: {duracion.total_seconds():.1f} segundos")
        print(f"📊 ESTADÍSTICAS:")
        print(f"   • Archivos encontrados: {self.resumen['total_archivos']}")
        print(f"   • Archivos procesados:  {self.resumen['procesados']}")
        print(f"   • Archivos omitidos:    {self.resumen['omitidos']}")
        print(f"   • Errores encontrados:  {len(self.resumen['errores'])}")
        
        # Resumen de diccionarios creados - SOLO .dic
        if self.resumen['diccionarios']:
            print(f"\n📚 DICCIONARIOS CREADOS ({len(self.resumen['diccionarios'])}):")
            print(f"{'-'*60}")
            
            for archivo, info in self.resumen['diccionarios'].items():
                print(f"\n📄 {archivo}:")
                print(f"   • Diccionario: {os.path.basename(info['archivo_dic'])}")
                print(f"   • Textos extraídos: {info['textos']}")
                print(f"   • Gráficas (ficheros) detectadas: {info['graficas']}")
        
        # Resumen de gráficas - SOLO FICHEROS
        total_ficheros = 0
        ficheros_por_archivo = {}
        
        for archivo, graficas in self.resumen['graficas'].items():
            ficheros = [g for g in graficas]  # Ya solo tenemos las que generan ficheros
            if ficheros:
                total_ficheros += len(ficheros)
                ficheros_por_archivo[archivo] = ficheros
        
        if total_ficheros > 0:
            print(f"\n💾 FICHEROS DE GRÁFICAS A GENERAR (Total: {total_ficheros}):")
            print(f"{'-'*60}")
            
            for archivo, ficheros in ficheros_por_archivo.items():
                print(f"\n   📁 {archivo}:")
                for g in ficheros:
                    print(f"      • {g['nombre']} (línea {g['linea']})")
        
        # Mostrar errores si los hay
        if self.resumen['errores']:
            print(f"\n⚠️  ERRORES ENCONTRADOS ({len(self.resumen['errores'])}):")
            for error in self.resumen['errores']:
                print(f"   • {error}")
        
        # Instrucciones finales
        print(f"\n{'='*80}")
        print("🎯 SIGUIENTES PASOS: enviar a uana AI el diccionario a traducir y ejecutar explorar.py")
        print(f"{'='*80}")
        
        if self.resumen['diccionarios']:
            print(f"\n1. 📝 TRADUCIR TEXTOS:")
            print(f"   • Los diccionarios están en: {self.DIC_DIR}")
            print(f"   • Formato: idioma;archivo;id;texto_traducido")
            
            print(f"\n2. 🚀 EJECUTAR GRÁFICAS:")
            for archivo, info in self.resumen['diccionarios'].items():
                if info['graficas'] > 0:
                    print(f"   • python {os.path.join(self.SRC_DIR, archivo)}")
                    print(f"     → Generará {info['graficas']} fichero(s) de gráfica")
            
            print(f"\n3. 📁 ARCHIVOS GENERADOS:")
            print(f"   • Diccionarios: {self.DIC_DIR} (archivos es-*.dic)")
            print(f"   • Gráficas: Se generarán en el directorio actual al ejecutar los scripts")
        else:
            print(f"\nℹ️  No se crearon diccionarios. Verifica que los archivos .py contengan textos.")
        
        print(f"\n{'='*80}")
        print(" " * 30 + "✅ PROCESO COMPLETADO")
        print(f"{'='*80}")
    
    # ------------------------------------------------------------
    

# ------------------------------------------------------------
# FUNCIÓN PRINCIPAL
# ------------------------------------------------------------

def main():
    """Función principal del programa"""
    
    # Verificar argumentos
    if len(sys.argv) < 2:
        print(f"\n❌ USO: python {os.path.basename(__file__)} [archivo.py | todos]")
        print(f"\n📖 EJEMPLOS:")
        print(f"   python {os.path.basename(__file__)} todos                    # Todos los archivos")
        print(f"   python {os.path.basename(__file__)} confinamiento.py        # Un archivo específico")
        print(f"\n📋 FUNCIONALIDADES:")
        print(f"   1. Extrae textos en español para traducción")
        print(f"   2. Detecta gráficas que generan ficheros (savefig, write_image, save)")
        print(f"   3. Crea diccionarios es-*.dic en ../dic/")
        print(f"   4. Muestra nombres de ficheros de gráficas a generar")
        sys.exit(1)
    
    archivo = sys.argv[1]
    
    try:
        # Crear y ejecutar gestor
        gestor = DiccionarioGraficas(archivo)
        gestor.ejecutar()
        
    except KeyboardInterrupt:
        print(f"\n\n🛑 PROCESO INTERRUMPIDO POR EL USUARIO")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()