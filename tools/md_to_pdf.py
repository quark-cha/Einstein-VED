import sys
import re
import tempfile
from pathlib import Path
import markdown
from playwright.sync_api import sync_playwright
import base64
import subprocess
import os

# =========================
# Configuración
# =========================
OUTPUT_PDF_DIR = "pdfs"

# =========================
# Plantilla HTML para PDF
# =========================
HTML_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
body {{
    font-family: "Noto Sans SC", sans-serif;
    line-height: 1.5;
    margin: 0;
    padding: 0;
    width: 100%;
}}
.container {{
    width: 100%;
    max-width: 100%;
    margin: 0 auto;
    padding: 15mm;
}}
img {{
    max-width: 100% !important;
    width: auto !important;
    height: auto !important;
    display: block;
    margin: 1em auto;
}}
pre {{
    background: #f6f8fa;
    padding: 10px;
    border-radius: 6px;
    overflow: auto;
    max-width: 100%;
}}
code {{ font-family: monospace; }}
table {{
    width: 100% !important;
    max-width: 100% !important;
    border-collapse: collapse;
}}
</style>
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']]
  }},
  svg: {{ fontCache: 'global' }},
  options: {{
    ignoreHtmlClass: 'tex2jax_ignore',
    processHtmlClass: 'tex2jax_process'
  }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
<div class="container">
__MD2PDF_BODY__
</div>
</body>
</html>
"""

# =========================
# FUNCIÓN PARA REESCRIBIR ENLACES
# =========================
def reescribir_enlaces(contenido_md, extension_destino):
    """
    Reemplaza enlaces a .md por la extensión destino (.pdf)
    Ejemplo: [texto](subdir/ES_24.md) → [texto](subdir/ES_24.pdf)
    """
    patron = r'\[([^\]]+)\]\(([^)]+)\.md(?:#([^)]+))?\)'
    
    def reemplazo(match):
        ruta = match.group(2)
        ancla = match.group(3) if match.group(3) else ""
        texto = f"{ruta}{extension_destino}"
        if ancla:
            return f"[{texto}]({ruta}{extension_destino}#{ancla})"
        else:
            return f"[{texto}]({ruta}{extension_destino})"
    
    return re.sub(patron, reemplazo, contenido_md)

# =========================
# Funciones comunes
# =========================
def strip_frontmatter(md_text: str) -> str:
    if md_text.startswith('---'):
        parts = md_text.split('---', 2)
        if len(parts) == 3:
            return parts[2].lstrip()
    return md_text

# =========================
# Funciones para PDF
# =========================
MATH_PLACEHOLDER = "MD2HTML_MATHPLC_{}"
math_store = []

def extract_math(text: str) -> str:
    """Extrae fórmulas y reemplaza por placeholders"""
    global math_store
    math_store = []

    def repl_dd(m):
        idx = len(math_store)
        math_store.append(("display", m.group(1)))
        return MATH_PLACEHOLDER.format(idx)
    text = re.sub(r"\$\$\s*([\s\S]+?)\s*\$\$", repl_dd, text)
    text = re.sub(r"\\\[\s*([\s\S]+?)\s*\\\]", repl_dd, text)

    def repl_in(m):
        idx = len(math_store)
        math_store.append(("inline", m.group(1)))
        return MATH_PLACEHOLDER.format(idx)
    text = re.sub(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", repl_in, text)

    return text

def restore_math(html: str) -> str:
    """Restaura placeholders para PDF usando MathJax"""
    def repl(m):
        idx = int(m.group(1))
        if idx < len(math_store):
            typ, code = math_store[idx]
            code_safe = code.replace("</script>", "<\\/script>")
            if typ == "inline":
                return f"\\({code_safe}\\)"
            else:
                return f"\\[{code_safe}\\]"
        else:
            return m.group(0)
    return re.sub(r"MD2HTML_MATHPLC_(\d+)", repl, html)

def get_image_mime_type(img_path: Path) -> str:
    ext = img_path.suffix.lower()
    mime_map = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.svg': 'image/svg+xml',
        '.mng': 'video/mng'
    }
    return mime_map.get(ext, 'application/octet-stream')

def embed_images(html: str, base_dir: Path) -> str:
    def repl(m):
        src = m.group(1).strip()
        if src.startswith("http") or src.startswith("data:"):
            return f'<img src="{src}" style="width:100%;max-width:100%;height:auto;display:block;margin:1em auto;" />'
        img_path = (base_dir / src).resolve()
        if not img_path.exists():
            return f'<div style="background:#ffebee;padding:10px;border:1px solid red;"> Imagen no encontrada: {src}</div>'
        try:
            if img_path.suffix.lower() == ".svg":
                svg_content = img_path.read_text(encoding="utf-8")
                if 'width=' not in svg_content:
                    svg_content = svg_content.replace("<svg ", '<svg width="100%" ')
                if 'height=' not in svg_content:
                    svg_content = svg_content.replace("<svg ", '<svg height="auto" ')
                if "viewBox=" not in svg_content:
                    svg_content = svg_content.replace("<svg ", '<svg viewBox="0 0 100 100" ')
                svg_encoded = base64.b64encode(svg_content.encode("utf-8")).decode("ascii")
                return f'<img src="data:image/svg+xml;base64,{svg_encoded}" style="width:100%;max-width:100%;height:auto;display:block;margin:1em auto;" />'
            mime_type = get_image_mime_type(img_path)
            data = base64.b64encode(img_path.read_bytes()).decode("ascii")
            return f'<img src="data:{mime_type};base64,{data}" style="width:100%;max-width:100%;height:auto;display:block;margin:1em auto;" />'
        except Exception:
            return f'<div style="background:#ffebee;padding:10px;border:1px solid red;"> Error cargando imagen: {src}</div>'
    return re.sub(r'<img[^>]*src="([^"]+)"[^>]*>', repl, html, flags=re.IGNORECASE)

# =========================
# md → PDF
# =========================
def md_to_pdf(md_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    out_pdf = output_dir / f"{md_path.stem}.pdf"

    md_text = md_path.read_text(encoding="utf-8", errors="replace")
    md_text = strip_frontmatter(md_text)
    
    md_text = reescribir_enlaces(md_text, ".pdf")
    
    no_math = extract_math(md_text)

    md = markdown.Markdown(extensions=["fenced_code", "tables"])
    html_body = md.convert(no_math)
    html_body = restore_math(html_body)
    html_body = embed_images(html_body, md_path.parent)
    full_html = HTML_TEMPLATE.replace("__MD2PDF_BODY__", html_body)

    tmp_html_path = output_dir / f"{md_path.stem}_temp.html"
    tmp_html_path.write_text(full_html, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({"width": 794, "height": 1123})
        page.goto(tmp_html_path.absolute().as_uri())
        page.wait_for_timeout(5000)
        try:
            page.evaluate("""
                if (window.MathJax) return MathJax.typesetPromise();
                return Promise.resolve();
            """)
            page.wait_for_timeout(2000)
        except:
            pass
        page.pdf(
            path=str(out_pdf),
            format="A4",
            print_background=True,
            margin={"top":"15mm","bottom":"15mm","left":"15mm","right":"15mm"},
            prefer_css_page_size=True
        )
        browser.close()
    
    tmp_html_path.unlink()
    print(f"📑 PDF generado: {out_pdf}")

# =========================
# Función principal
# =========================
def main():
    if len(sys.argv) < 2:
        print("Uso: python md_to_pdf.py archivo.md | todos")
        sys.exit(1)

    args = sys.argv[1:]
    base_dir = Path(__file__).resolve().parent
    md_dir = base_dir.parent
    
    print(f"🔍 Buscando archivos .md en: {md_dir.absolute()}")
    
    pdf_dir = base_dir / OUTPUT_PDF_DIR

    if len(args)==1 and args[0].lower()=="todos":
        md_files = list(md_dir.glob("*.md"))
        
        if not md_files:
            print("❌ No hay archivos .md en:", md_dir)
            sys.exit(1)
        
        print(f"🎯 Procesando {len(md_files)} archivos .md...\n")
        
        for md_file in sorted(md_files):
            print(f"▶ Procesando: {md_file.name}")
            md_to_pdf(md_file, pdf_dir)
        
        print(f"\n📊 Resumen: PDFs generados: {len(md_files)}")
        return

    # Modo archivo individual
    for arg in args:
        if not arg.endswith(".md"):
            print(f"⚠️ Ignorando {arg}: no es un archivo .md")
            continue
        md_file = md_dir / arg
        if not md_file.exists():
            print(f"❌ {md_file} no existe")
            continue
        
        print(f"▶ Procesando: {md_file.name}")
        md_to_pdf(md_file, pdf_dir)

if __name__ == "__main__":
    main()