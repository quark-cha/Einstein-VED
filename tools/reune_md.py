import re
import argparse
from pathlib import Path

# Idiomas soportados
IDIOMAS_SOPORTADOS = ['ES', 'EN', 'FR', 'DE', 'IT', 'PT', 'RU', 'ZH', 'JA']

# Nombre base del archivo de salida
NOMBRE_BASE = "EINSTEIN-VED"  # Cambiado de UNIHOLOG a EINSTEIN-VED

def extraer_numero(nombre):
    """
    Extrae el número del nombre del archivo.
    Soporta: ES_0.md, ES_0_Einstein-VED.md, EN_12_articulo.md, etc.
    """
    match = re.search(r'(?:' + '|'.join(IDIOMAS_SOPORTADOS) + r')_(\d+)', nombre, re.IGNORECASE)
    return int(match.group(1)) if match else 9999

def extraer_idioma(nombre):
    """Extrae el idioma del nombre del archivo (ES, EN, FR, etc.)"""
    match = re.search(r'^(' + '|'.join(IDIOMAS_SOPORTADOS) + r')_', nombre, re.IGNORECASE)
    return match.group(1).upper() if match else None

def buscar_archivos(origen_raiz, idioma):
    """
    Busca archivos MD del idioma especificado en:
    1. Directorio raíz
    2. Subdirectorio papers/
    """
    archivos = []
    origen_path = Path(origen_raiz)
    
    # Buscar en raíz
    archivos_raiz = list(origen_path.glob(f"{idioma}_*.md"))
    archivos.extend(archivos_raiz)
    
    # Buscar en papers/
    papers_path = origen_path / "papers"
    if papers_path.exists():
        archivos_papers = list(papers_path.glob(f"{idioma}_*.md"))
        archivos.extend(archivos_papers)
    
    # Eliminar duplicados (si mismo nombre en raíz y papers)
    unicos = {}
    for a in archivos:
        unicos[a.name] = a
    archivos = list(unicos.values())
    
    return archivos

def concatenar_md(origen_raiz, idioma, output_dir=None):
    """
    Concatena todos los archivos MD de un idioma en un solo EINSTEIN-VED.md
    """
    origen_path = Path(origen_raiz)
    if not origen_path.exists():
        print(f"❌ Error: No existe {origen_raiz}")
        return False
    
    if output_dir is None:
        output_dir = origen_path
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Nombre de salida: ES_EINSTEIN-VED.md, EN_EINSTEIN-VED.md, etc.
    salida = output_path / f"{idioma}_{NOMBRE_BASE}.md"
    
    archivos = buscar_archivos(origen_raiz, idioma)
    
    if not archivos:
        print(f"⚠️ No se encontraron archivos {idioma}_*.md en {origen_raiz} ni en papers/")
        return False
    
    # Orden numérico
    archivos.sort(key=lambda x: (extraer_numero(x.name), x.name))
    
    print(f"\n📄 Generando {salida.name} con {len(archivos)} archivos...")
    print(f"   (desde raíz y papers/)")
    for a in archivos:
        ruta = a.relative_to(origen_path) if origen_path in a.parents else a.name
        print(f"   - {ruta} (número {extraer_numero(a.name)})")
    
    contenido = []
    for a in archivos:
        ruta_relativa = a.relative_to(origen_path) if origen_path in a.parents else a.name
        contenido.append(f"\n\n---\n# Fuente: {ruta_relativa}\n---\n\n")
        contenido.append(a.read_text(encoding='utf-8'))
    
    salida_path = output_path / salida.name
    salida_path.write_text("\n".join(contenido), encoding='utf-8')
    print(f"✅ {salida.name} generado en {salida_path}")
    print(f"   Tamaño: {salida_path.stat().st_size:,} bytes")
    return True

def generar_todos(origen_raiz, output_dir=None, idiomas=None):
    """
    Genera EINSTEIN-VED para todos los idiomas encontrados.
    """
    if idiomas is None:
        idiomas = IDIOMAS_SOPORTADOS
    
    origen_path = Path(origen_raiz)
    if not origen_path.exists():
        print(f"❌ Error: No existe {origen_raiz}")
        return
    
    # Detectar qué idiomas tienen archivos
    idiomas_encontrados = set()
    for idioma in idiomas:
        archivos = buscar_archivos(origen_raiz, idioma)
        if archivos:
            idiomas_encontrados.add(idioma)
    
    if not idiomas_encontrados:
        print("❌ No se encontraron archivos de ningún idioma")
        return
    
    print("=" * 60)
    print(f"🔍 Idiomas detectados: {', '.join(sorted(idiomas_encontrados))}")
    print("=" * 60)
    
    for idioma in sorted(idiomas_encontrados):
        concatenar_md(origen_raiz, idioma, output_dir)
    
    print("\n✅ Proceso completado")

def main():
    parser = argparse.ArgumentParser(
        description='Genera EINSTEIN-VED.md (recopilación) para múltiples idiomas'
    )
    parser.add_argument('origen', nargs='?', default='.', 
                       help='Directorio raíz donde están los archivos MD (por defecto: .)')
    parser.add_argument('--output', '-o', default=None,
                       help='Directorio de salida (por defecto: mismo que origen)')
    parser.add_argument('--idioma', '-i', default=None,
                       help='Idioma específico (ES, EN, etc.). Si no se especifica, genera todos')
    args = parser.parse_args()
    
    if args.idioma:
        if args.idioma.upper() not in IDIOMAS_SOPORTADOS:
            print(f"❌ Idioma no soportado: {args.idioma}")
            print(f"   Idiomas soportados: {IDIOMAS_SOPORTADOS}")
            return
        concatenar_md(args.origen, args.idioma.upper(), args.output)
    else:
        generar_todos(args.origen, args.output)

if __name__ == "__main__":
    main()