import os
import csv
import glob
import subprocess
import re
from collections import defaultdict

class GestorTraducciones:
    def __init__(self):
        self.archivo_espanol = "español.csv"
        self.archivo_multi_idioma = "diccionario.csv"
        self.idiomas_objetivo = ['en', 'fr', 'de', 'it']
        
        # Archivos que deben ser excluidos del escaneo
        self.archivos_excluidos = [
            'diccionario.py', 'explorar.py', 'explorar_por_texto.py',
            # Derivados de diccionario
            'diccionario_', 'diccionario.', '_diccionario', 
            # Derivados de explorar
            'explorar_', 'explorar.', '_explorar',
            # Archivos de traducciones generados
            'español.csv', 'diccionario.csv', 'traducciones.json',
            'faltantes_', 'faltantes.', '_faltantes'
        ]
        
        # Palabras en inglés que deben ser eliminadas del español.csv
        self.palabras_ingles = [
            'bold', 'top', 'bottom', 'red', 'of', 'on', 'center', 'green', 
            'enter', 'equal', 'right', 'svg', 'png', 'jpeg', 'blue', 'orange',
            'left', 'save', 'load', 'file', 'edit', 'view', 'help', 'tools',
            'settings', 'options', 'window', 'menu', 'button', 'label', 'text',
            'input', 'output', 'data', 'plot', 'chart', 'graph', 'axis', 'title',
            'legend', 'grid', 'color', 'size', 'width', 'height', 'margin',
            'padding', 'border', 'background', 'font', 'style', 'class', 'id',
            'function', 'method', 'variable', 'constant', 'parameter', 'return',
            'import', 'export', 'module', 'package', 'library', 'framework',
            'database', 'server', 'client', 'network', 'protocol', 'api',
            'json', 'xml', 'html', 'css', 'javascript', 'python', 'java',
            'c++', 'c#', 'php', 'ruby', 'sql', 'nosql', 'mysql', 'postgresql',
            'mongodb', 'redis', 'docker', 'kubernetes', 'aws', 'azure', 'gcp'
        ]
        
        # Verificar y crear español.csv si no existe
        if not os.path.exists(self.archivo_espanol):
            print("🔍 español.csv no encontrado.")
            self.crear_espanol_opciones()

    # ====== SISTEMA CON ID = LÍNEA ======
    def crear_espanol_con_lineas(self):
        """Crea español.csv usando número de línea como ID"""
        print("📝 Creando español.csv con ID = número de línea...")
        
        textos = self.escanear_archivos_py_con_lineas()
        
        if not textos:
            print("❌ No se encontraron textos para traducir")
            return False
        
        with open(self.archivo_espanol, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['idioma', 'archivo', 'id', 'texto_traducido'])
            
            for texto_info in textos:
                writer.writerow([
                    'es',
                    texto_info['archivo'],
                    texto_info['id'],  # ID = número de línea
                    texto_info['texto']
                ])
        
        print(f"✅ Creado {self.archivo_espanol} con {len(textos)} entradas")
        print("💡 ID = número de línea donde se encontró el texto")
        self.mostrar_estadisticas_detalladas()
        return True

    def escanear_archivos_py_con_lineas(self):
        """Escanea archivos .py usando número de línea como ID"""
        print("📁 Escaneando archivos .py (ID = línea)...")
        archivos_py = glob.glob(os.path.join(".", "*.py"))
        textos_encontrados = []
        
        archivos_procesados = 0
        archivos_excluidos = 0
        
        for archivo in archivos_py:
            nombre_archivo = os.path.basename(archivo)
            
            if self._es_archivo_excluido(nombre_archivo):
                print(f"   ⏭️  Excluyendo: {nombre_archivo}")
                archivos_excluidos += 1
                continue
            
            print(f"   📄 Analizando: {nombre_archivo}")
            archivos_procesados += 1
            
            textos = self.extraer_textos_espanol_con_lineas(archivo)
            textos_encontrados.extend(textos)
            
            print(f"      ✅ {len(textos)} textos encontrados")
        
        print(f"\n📊 RESUMEN DEL ESCANEO:")
        print(f"   📁 Archivos .py encontrados: {len(archivos_py)}")
        print(f"   ✅ Archivos procesados: {archivos_procesados}")
        print(f"   ⏭️  Archivos excluidos: {archivos_excluidos}")
        print(f"   🎯 Textos encontrados: {len(textos_encontrados)}")
        
        return textos_encontrados

    def extraer_textos_espanol_con_lineas(self, ruta_archivo):
        """Extrae textos usando número de línea como ID"""
        textos = []
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
        
            nombre_archivo = os.path.basename(ruta_archivo)
            
            for num_linea, linea in enumerate(lineas, 1):
                # Extraer entre comillas dobles
                i = 0
                while i < len(linea):
                    if linea[i] == '"':
                        start = i + 1
                        i += 1
                        while i < len(linea) and linea[i] != '"':
                            i += 1
                        if i < len(linea):
                            texto = linea[start:i]
                            if self._es_texto_valido(texto):
                                # ID = número de línea con 4 dígitos
                                id_texto = f"{num_linea:04d}"
                                textos.append({
                                    'archivo': nombre_archivo,
                                    'id': id_texto,
                                    'texto': texto.strip(),
                                    'linea_original': num_linea
                                })
                            i += 1
                    else:
                        i += 1
                
                # Extraer entre comillas simples
                i = 0
                while i < len(linea):
                    if linea[i] == "'":
                        start = i + 1
                        i += 1
                        while i < len(linea) and linea[i] != "'":
                            i += 1
                        if i < len(linea):
                            texto = linea[start:i]
                            if self._es_texto_valido(texto):
                                # ID = número de línea con 4 dígitos
                                id_texto = f"{num_linea:04d}"
                                textos.append({
                                    'archivo': nombre_archivo,
                                    'id': id_texto,
                                    'texto': texto.strip(),
                                    'linea_original': num_linea
                                })
                            i += 1
                    else:
                        i += 1
                        
        except Exception as e:
            print(f"❌ Error extrayendo textos de {ruta_archivo}: {e}")
        
        return textos

    def _es_texto_valido(self, texto):
        """Verifica si el texto es válido para traducción"""
        texto_limpio = texto.strip()
        if not texto_limpio:
            return False
        
        # EXCLUSIONES BÁSICAS
        exclusiones_basicas = [".png", ".jpg", ".jpeg", ".svg", ".gif", ".pdf", ".eps", "savefig"]
        texto_lower = texto_limpio.lower()
        if any(ext in texto_lower for ext in exclusiones_basicas):
            return False
        
        # VERIFICAR LONGITUD MÍNIMA
        if len(texto_limpio) < 3:
            return False
        
        # VERIFICAR SI ES SOLO NÚMEROS
        if texto_limpio.replace('.', '').replace(',', '').replace(' ', '').isdigit():
            return False
        
        # VERIFICAR COLORES HEXADECIMALES
        if re.match(r'^#[0-9A-Fa-f]{3,8}$', texto_limpio):
            return False
        
        # VERIFICAR SI ES CÓDIGO
        patrones_codigo = [
            r'^[a-z_]+$', r'^[A-Z_]+$', r'^[a-z]+[A-Z][a-zA-Z]*$',
            r'^[a-zA-Z0-9_]+$', r'^[a-zA-Z]+[0-9]+$', r'^[0-9]+[a-zA-Z]+$',
        ]
        for patron in patrones_codigo:
            if re.match(patron, texto_limpio):
                return False
        
        # VERIFICAR PORCENTAJE DE LETRAS
        letras = sum(1 for c in texto_limpio if c.isalpha())
        if letras / len(texto_limpio) < 0.4:
            return False
        
        # VERIFICAR PALABRAS EN INGLÉS
        palabras = texto_lower.split()
        if palabras:
            if any(palabra in self.palabras_ingles for palabra in palabras):
                return False
            palabras_ingles = sum(1 for palabra in palabras if palabra in self.palabras_ingles)
            if palabras_ingles / len(palabras) > 0.3:
                return False
        
        return True

    # ====== GENERACIÓN DE ARCHIVOS PARA IA ======
    def generar_archivo_faltantes(self, idioma):
        """Genera archivo para IA con la cabecera especificada"""
        print(f"\n📁 GENERANDO ARCHIVO PARA {idioma.upper()}")
        print("="*50)
        
        faltantes_por_archivo_idioma = self.analizar_faltantes_detallado()
        
        if not faltantes_por_archivo_idioma:
            print(f"✅ No hay traducciones faltantes para {idioma}")
            return
        
        todas_faltantes = []
        for archivo, idiomas_data in faltantes_por_archivo_idioma.items():
            if idioma in idiomas_data:
                for falta in idiomas_data[idioma]:
                    todas_faltantes.append({
                        'archivo': archivo,
                        'id': falta['id'],  # ID = número de línea
                        'texto_espanol': falta['texto_espanol']
                    })
        
        if not todas_faltantes:
            print(f"✅ No hay traducciones faltantes para {idioma}")
            return
        
        archivo_salida = f"faltantes_{idioma}.csv"
        
        with open(archivo_salida, 'w', encoding='utf-8', newline='') as f:
            # Escribir cabecera para IA
            f.write("# INSTRUCCIONES PARA LA IA:\n")
            f.write("# - Formato: \n")
            f.write("# Entrada:\n")
            f.write("#     es;<archivo>;<id>;<texto_español>\n")
            f.write("# Salida:\n")
            f.write("# <idioma>;<archivo>;<id>;<texto_traducido>\n")
            f.write("# Respetar los campos \n")
            f.write("#   <archivo> e <id>\n")
            f.write("# Poner el texto de la traduccion en <texto_traducido>\n")
            f.write("# Importante en caso de que no haya traduccion\n")
            f.write("# o no sea posible dejar en <texto_traducido> el <texto_español>\n")
            f.write("# Respetar formulas, formatos, caracteres especiales y saltos de línea tal como \n")
            f.write("# están en el texto español.\n")
            f.write("#  - Traducir del español al idioma indicado\n")
            f.write("\n")
            f.write("# TRADUCCIONES FALTANTES:\n")
            f.write("# lo que sigue son las lineas del diccionario español que no tienen su entrada en el idioma que se esta pidiendo\n")
            f.write("\n")
            
            # Escribir encabezado del CSV
            f.write("idioma;archivo;id;texto_traducido\n")
            
            # Escribir las entradas faltantes
            for falta in todas_faltantes:
                # Formato: es;archivo.py;0123;texto español
                linea = f"es;{falta['archivo']};{falta['id']};{falta['texto_espanol']}\n"
                f.write(linea)
        
        print(f"✅ Archivo generado: {archivo_salida}")
        print(f"📝 Total entradas faltantes: {len(todas_faltantes)}")
        
        # Mostrar estadísticas
        archivos_afectados = set(falta['archivo'] for falta in todas_faltantes)
        print(f"📁 Archivos afectados: {len(archivos_afectados)}")
        
        print(f"\n💡 INSTRUCCIONES:")
        print(f"1. Archivo: {archivo_salida}")
        print(f"2. La IA debe completar las traducciones en la columna 'texto_traducido'")
        print(f"3. Formato de salida: {idioma};archivo.py;id;texto_traducido")
        print(f"4. Si no puede traducir, dejar el texto español original")
        print(f"5. Conservar formatos, fórmulas y caracteres especiales")

    def importar_traducciones(self, archivo_traducciones, idioma):
        """Importa traducciones desde archivo completado por la IA"""
        if not os.path.exists(archivo_traducciones):
            print(f"❌ No se encuentra {archivo_traducciones}")
            return
        
        print(f"\n📥 IMPORTANDO TRADUCCIONES DE IA PARA {idioma.upper()}")
        print("="*50)
        
        nuevas_traducciones = []
        lineas_procesadas = 0
        
        with open(archivo_traducciones, 'r', encoding='utf-8') as f:
            for linea in f:
                lineas_procesadas += 1
                
                # Saltar líneas de comentario
                if linea.strip().startswith('#') or not linea.strip():
                    continue
                
                # Procesar línea: idioma;archivo;id;texto_traducido
                partes = linea.strip().split(';')
                if len(partes) >= 4:
                    idioma_linea = partes[0].strip()
                    archivo = partes[1].strip()
                    id_texto = partes[2].strip()
                    texto_traducido = partes[3].strip()
                    
                    # Verificar que sea la línea correcta y tenga traducción
                    if idioma_linea == idioma and texto_traducido:
                        nuevas_traducciones.append({
                            'idioma': idioma,
                            'archivo': archivo,
                            'id': id_texto,
                            'texto': texto_traducido
                        })
        
        print(f"📊 Líneas procesadas: {lineas_procesadas}")
        print(f"📝 Traducciones válidas encontradas: {len(nuevas_traducciones)}")
        
        if not nuevas_traducciones:
            print("❌ No se encontraron traducciones válidas")
            return
        
        # Cargar diccionario actual
        datos_multi = self.cargar_csv(self.archivo_multi_idioma)
        
        # Actualizar o agregar entradas
        actualizadas = 0
        nuevas = 0
        
        for nueva in nuevas_traducciones:
            encontrado = False
            for i, entrada in enumerate(datos_multi):
                if (entrada['archivo'] == nueva['archivo'] and 
                    entrada['id'] == nueva['id'] and 
                    entrada['idioma'] == nueva['idioma']):
                    datos_multi[i]['texto'] = nueva['texto']
                    encontrado = True
                    actualizadas += 1
                    break
            
            if not encontrado:
                datos_multi.append(nueva)
                nuevas += 1
        
        # Guardar diccionario actualizado
        with open(self.archivo_multi_idioma, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['idioma', 'archivo', 'id', 'texto_traducido'])
            for entrada in datos_multi:
                writer.writerow([
                    entrada['idioma'],
                    entrada['archivo'],
                    entrada['id'],
                    entrada['texto']
                ])
        
        print(f"✅ IMPORTACIÓN COMPLETADA:")
        print(f"   🔄 Entradas actualizadas: {actualizadas}")
        print(f"   ➕ Entradas nuevas: {nuevas}")
        print(f"   📊 Total en diccionario: {len(datos_multi)} entradas")

    # ====== ANÁLISIS DE TRADUCCIONES ======
    def analizar_faltantes_detallado(self):
        """Analiza traducciones faltantes con IDs de línea"""
        print("\n🔍 ANALIZANDO TRADUCCIONES FALTANTES...")
        
        if not os.path.exists(self.archivo_espanol):
            print("❌ español.csv no encontrado")
            self.crear_espanol_opciones()
            return {}
        
        datos_espanol = self.cargar_csv(self.archivo_espanol)
        datos_multi = self.cargar_csv(self.archivo_multi_idioma)
        
        if not datos_espanol:
            print("❌ No hay datos en español.csv")
            return {}
        
        print(f"📊 Español: {len(datos_espanol)} entradas")
        print(f"📊 Multi-idioma: {len(datos_multi)} entradas")
        
        # Crear índice usando archivo + ID (línea)
        indice_multi = defaultdict(dict)
        for entrada in datos_multi:
            clave = f"{entrada['archivo']};{entrada['id']}"  # archivo;0123
            indice_multi[clave][entrada['idioma']] = entrada['texto']
        
        faltantes_por_archivo_idioma = defaultdict(lambda: defaultdict(list))
        
        for entrada_es in datos_espanol:
            archivo = entrada_es['archivo']
            clave = f"{archivo};{entrada_es['id']}"  # archivo.py;0123
            texto_espanol = entrada_es['texto']
            
            for idioma in self.idiomas_objetivo:
                if clave not in indice_multi or idioma not in indice_multi[clave] or not indice_multi[clave][idioma].strip():
                    faltantes_por_archivo_idioma[archivo][idioma].append({
                        'id': entrada_es['id'],  # ID = número de línea
                        'texto_espanol': texto_espanol
                    })
        
        # Mostrar resultados
        total_faltantes = 0
        print(f"\n📁 ANÁLISIS POR ARCHIVO:")
        
        for archivo in sorted(faltantes_por_archivo_idioma.keys()):
            print(f"\n📄 {archivo}:")
            
            for idioma in self.idiomas_objetivo:
                if idioma in faltantes_por_archivo_idioma[archivo]:
                    faltantes = faltantes_por_archivo_idioma[archivo][idioma]
                    total_faltantes += len(faltantes)
                    print(f"   🌍 {idioma.upper()}: {len(faltantes)} faltantes")
                    
                    # Mostrar algunos ejemplos con IDs
                    for i, falta in enumerate(faltantes[:2], 1):
                        print(f"      {i}. 📍 ID:{falta['id']} | '{falta['texto_espanol'][:40]}...'")
        
        print(f"\n🎯 RESUMEN GENERAL:")
        print(f"📁 Archivos con traducciones faltantes: {len(faltantes_por_archivo_idioma)}")
        print(f"🌍 Total traducciones faltantes: {total_faltantes}")
        
        return faltantes_por_archivo_idioma

    # ====== FUNCIONES AUXILIARES ======
    def _es_archivo_excluido(self, nombre_archivo):
        """Verifica si un archivo debe ser excluido"""
        nombre_lower = nombre_archivo.lower()
        for exclusion in self.archivos_excluidos:
            if exclusion in nombre_lower:
                return True
        return False

    def cargar_csv(self, archivo):
        """Carga archivo CSV"""
        if not os.path.exists(archivo):
            return []
        
        datos = []
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                encabezados = next(reader)
            except:
                return []
            
            for fila in reader:
                if len(fila) >= 4:
                    datos.append({
                        'idioma': fila[0].strip(),
                        'archivo': fila[1].strip(),
                        'id': fila[2].strip(),
                        'texto': fila[3].strip()
                    })
        return datos

    def crear_espanol_opciones(self):
        """Opciones para crear español.csv"""
        print("\n🆕 OPCIONES PARA CREAR español.csv:")
        print("1. 🆕 Crear con ID = línea (recomendado)")
        print("2. 🔄 Usar explorar.py")
        print("3. 📁 Desde diccionario.csv")
        
        opcion = input("👉 Selecciona: ").strip()
        
        if opcion == "1":
            self.crear_espanol_con_lineas()
        elif opcion == "2":
            self.crear_espanol_desde_explorar()
        elif opcion == "3":
            self.regenerar_espanol_desde_diccionario()
        else:
            self.crear_espanol_con_lineas()

    def crear_espanol_desde_explorar(self):
        """Crea desde explorar.py"""
        print("🚀 Ejecutando explorar.py...")
        try:
            subprocess.run(['python', 'explorar.py'], capture_output=True)
            if os.path.exists("diccionario.csv"):
                self.regenerar_espanol_desde_diccionario()
        except:
            self.crear_espanol_con_lineas()

    def regenerar_espanol_desde_diccionario(self):
        """Regenera desde diccionario.csv"""
        if not os.path.exists(self.archivo_multi_idioma):
            print("❌ diccionario.csv no encontrado")
            return
        
        datos = self.cargar_csv(self.archivo_multi_idioma)
        entradas_es = [e for e in datos if e['idioma'] == 'es']
        
        if not entradas_es:
            print("❌ No hay entradas en español")
            return
        
        with open(self.archivo_espanol, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['idioma', 'archivo', 'id', 'texto_traducido'])
            for entrada in entradas_es:
                writer.writerow([entrada['idioma'], entrada['archivo'], entrada['id'], entrada['texto']])
        
        print(f"✅ Regenerado con {len(entradas_es)} entradas")

    def mostrar_estadisticas_detalladas(self):
        """Muestra estadísticas"""
        datos = self.cargar_csv(self.archivo_espanol)
        if not datos:
            return
        
        archivos = set(e['archivo'] for e in datos)
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"   📈 Entradas: {len(datos)}")
        print(f"   📁 Archivos: {len(archivos)}")
        print(f"   📍 IDs: números de línea (ej: {datos[0]['id']})")

    def limpiar_entradas_vacias(self, archivo_a_limpiar=None):
        """Limpia entradas vacías"""
        if archivo_a_limpiar is None:
            print("\n🧹 LIMPIAR ENTRADAS VACÍAS")
            print("1. Limpiar diccionario.csv")
            print("2. Limpiar español.csv")
            opcion = input("👉 Selecciona: ").strip()
            archivo_a_limpiar = self.archivo_multi_idioma if opcion == "1" else self.archivo_espanol
        
        if not os.path.exists(archivo_a_limpiar):
            print(f"❌ No se encuentra {archivo_a_limpiar}")
            return
        
        with open(archivo_a_limpiar, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            encabezados = next(reader)
            datos = [fila for fila in reader if len(fila) >= 4 and fila[3].strip()]
        
        with open(archivo_a_limpiar, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(encabezados)
            writer.writerows(datos)
        
        print(f"✅ Limpiado {archivo_a_limpiar}")

    def mostrar_menu_principal(self):
        print("\n" + "="*50)
        print("🎯 GESTOR DE TRADUCCIONES - SISTEMA POR LÍNEA")
        print("="*50)
        print("1. 🔍 ANALIZAR TRADUCCIONES FALTANTES")
        print("2. 📁 GENERAR ARCHIVO PARA IA")
        print("3. 📥 IMPORTAR TRADUCCIONES DE IA")
        print("4. 🧹 LIMPIAR ENTRADAS VACÍAS")
        print("5. 🆕 CREAR español.csv (ID = línea)")
        print("6. 🌍 CONFIGURAR IDIOMAS")
        print("0. 🚪 SALIR")
        print("="*50)

def main():
    print("🚀 GESTOR DE TRADUCCIONES - ID = NÚMERO DE LÍNEA")
    gestor = GestorTraducciones()
    
    while True:
        gestor.mostrar_menu_principal()
        opcion = input("👉 Selecciona opción: ").strip()
        
        if opcion == "1":
            gestor.analizar_faltantes_detallado()
        elif opcion == "2":
            print(f"\n🌍 IDIOMAS: {gestor.idiomas_objetivo}")
            idioma = input("👉 Idioma para IA: ").strip().lower()
            if idioma in gestor.idiomas_objetivo:
                gestor.generar_archivo_faltantes(idioma)
        elif opcion == "3":
            archivo = input("📁 Archivo con traducciones: ").strip()
            idioma = input("🌍 Idioma: ").strip().lower()
            gestor.importar_traducciones(archivo, idioma)
        elif opcion == "4":
            gestor.limpiar_entradas_vacias()
        elif opcion == "5":
            gestor.crear_espanol_opciones()
        elif opcion == "6":
            print(f"🌍 Idiomas actuales: {gestor.idiomas_objetivo}")
            nuevos = input("👉 Nuevos idiomas (separados por coma): ").strip()
            if nuevos:
                gestor.idiomas_objetivo = [idioma.strip().lower() for idioma in nuevos.split(',')]
                print(f"✅ Actualizados: {gestor.idiomas_objetivo}")
        elif opcion == "0":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida")
        
        input("\n⏎ Presiona Enter para continuar...")

if __name__ == "__main__":
    main()