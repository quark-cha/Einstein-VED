import sys
import re
import tempfile
from pathlib import Path
import markdown
from playwright.sync_api import sync_playwright
import base64
import matplotlib as mpl

# =========================
# Configuración de Matplotlib para CJK
# =========================
#mpl.rcParams['font.family'] = 'Noto Sans CJK SC'
#mpl.rcParams['svg.fonttype'] = 'none'

# =========================
# Plantilla HTML segura
# =========================
HTML_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">

<!-- Fuente CJK para todo el PDF -->
<!link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">

<style>
* {{
    box-sizing: border-box;
}}
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
img[src*="data:image"] {{
    max-width: 100% !important;
    width: auto !important;
    height: auto !important;
}}
img[src*="svg"] {{
    max-width: 100% !important;
    width: 100% !important;
    height: auto !important;
}}
pre {{
    background: #f6f8fa;
    padding: 10px;
    border-radius: 6px;
    overflow: auto;
    max-width: 100%;
}}
code {{
    font-family: monospace;
}}
table {{
    width: 100% !important;
    max-width: 100% !important;
    border-collapse: collapse;
}}
figure {{
    width: 100%;
    margin: 1em 0;
}}
figure img {{
    width: 100% !important;
    max-width: 100% !important;
}}
@media print {{
    body {{
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }}
    .container {{
        width: 100% !important;
        max-width: 100% !important;
        padding: 15mm !important;
    }}
    img {{
        max-width: 100% !important;
        width: auto !important;
        height: auto !important;
        page-break-inside: avoid;
    }}
    img[src*="svg"] {{
        width: 100% !important;
        max-width: 100% !important;
    }}
}}
</style>

<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['\\\\(','\\\\)'], ['$', '$']],
    displayMath: [['$$','$$'], ['\\\\[','\\\\]']]
  }},
  svg: {{ fontCache: 'global' }}
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
# Quitar frontmatter YAML
# =========================
def strip_frontmatter(md_text: str) -> str:
    if md_text.startswith('---'):
        parts = md_text.split('---', 2)
        if len(parts) == 3:
            return parts[2].lstrip()
    return md_text

# =========================
# Manejo de matemáticas
# =========================
MATH_PLACEHOLDER = "MD2HTML_MATHPLC_{}"
math_store = []

def extract_math(text: str) -> str:
    r"""Extrae $...$, $$...$$ y \[...\] como placeholders."""
    global math_store
    math_store = []

    def repl_dd(m):
        idx = len(math_store)
        math_store.append(("display", m.group(1)))
        return MATH_PLACEHOLDER.format(idx)
    text = re.sub(r"\$\$\s*([\s\S]+?)\s*\$\$", repl_dd, text)

    def repl_br(m):
        idx = len(math_store)
        math_store.append(("display", m.group(1)))
        return MATH_PLACEHOLDER.format(idx)
    text = re.sub(r"\\\[\s*([\s\S]+?)\s*\\\]", repl_br, text)

    def repl_in(m):
        idx = len(math_store)
        math_store.append(("inline", m.group(1)))
        return MATH_PLACEHOLDER.format(idx)
    text = re.sub(r"(?<!\$)\$(?!\$)([^$\n]+?)(?<!\$)\$(?!\$)", repl_in, text)

    return text

def restore_math(html: str) -> str:
    def repl(m):
        idx = int(m.group(1))
        typ, code = math_store[idx]
        code_safe = code.replace("</script>", "<\\/script>")
        return f"\\({code_safe}\\)" if typ == "inline" else f"\\[{code_safe}\\]"
    return re.sub(r"MD2HTML_MATHPLC_(\d+)", repl, html)

# =========================
# Manejo de imágenes
# =========================
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
            return m.group(0)
        
        img_path = (base_dir / src).resolve()
        if not img_path.exists():
            return f'<div style="background:#ffebee; padding:10px; border:1px solid red;"> Imagen no encontrada: {src}</div>'
        
        try:
            if img_path.suffix.lower() == '.svg':
                svg_content = img_path.read_text(encoding='utf-8')
                if 'width=' not in svg_content and 'viewBox=' not in svg_content:
                    svg_content = svg_content.replace('<svg ', '<svg width="100%" height="auto" ')
                svg_encoded = base64.b64encode(svg_content.encode('utf-8')).decode('ascii')
                return f'<img src="data:image/svg+xml;base64,{svg_encoded}" style="max-width:100%; height:auto;">'
            else:
                mime_type = get_image_mime_type(img_path)
                data = base64.b64encode(img_path.read_bytes()).decode('ascii')
                return f'<img src="data:{mime_type};base64,{data}" style="max-width:100%; height:auto;">'
        except Exception as e:
            return f'<div style="background:#ffebee; padding:10px; border:1px solid red;"> Error cargando imagen: {src}</div>'
    
    return re.sub(r'<img[^>]*src="([^"]+)"[^>]*>', repl, html, flags=re.IGNORECASE)

# =========================
# Conversión Markdown -> PDF
# =========================
def md_to_pdf(md_path: Path):
    out_pdf = md_path.with_suffix(".pdf")
    md_text = md_path.read_text(encoding="utf-8")
    md_text = strip_frontmatter(md_text)

    no_math = extract_math(md_text)

    md = markdown.Markdown(extensions=["fenced_code", "tables"])
    html_body = md.convert(no_math)

    html_body = restore_math(html_body)
    html_body = embed_images(html_body, md_path.parent)

    full_html = HTML_TEMPLATE.replace("__MD2PDF_BODY__", html_body)

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".html", delete=False) as f:
        tmp_html_path = Path(f.name)
        f.write(full_html)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({"width": 794, "height": 1123})
        page.goto(tmp_html_path.as_uri())
        page.wait_for_timeout(5000)
        try:
            page.evaluate("""
                if (window.MathJax) {
                    return MathJax.typesetPromise();
                }
                return Promise.resolve();
            """)
            page.wait_for_timeout(2000)
        except Exception:
            pass
        page.pdf(
            path=str(out_pdf), 
            format="A4", 
            print_background=True,
            margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
            prefer_css_page_size=True
        )
        browser.close()

    try:
        tmp_html_path.unlink()
    except Exception:
        pass

    print(f" PDF generado: {out_pdf}")

# =========================
# Main
# =========================
def main():
    if len(sys.argv) < 2:
        print("Uso: python md_to_pdf.py archivo.md")
        sys.exit(1)
    md_file = Path(sys.argv[1])
    if not md_file.exists():
        print(f"ERROR: no existe {md_file}")
        sys.exit(1)
    md_to_pdf(md_file)

if __name__ == "__main__":
    main()
