import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as fm

import matplotlib as mpl

mpl.rcParams.update({
    'font.family': 'Noto Sans',
    'font.sans-serif': ['Noto Sans CJK SC'],
    'mathtext.fontset': 'dejavusans',
})

def configurar_fuentes(idioma, plt=None):
    """
    Configura la fuente de matplotlib según el idioma.
    Usa DejaVu Sans como fallback si no se encuentra la fuente principal.
    """
    fuentes_por_idioma = {
        "ja": ['Yu Gothic', 'Meiryo', 'MS Gothic', 'MS Mincho', 'DejaVu Sans'],
        "zh": [ 'SimSun', 'Microsoft YaHei','DejaVu Sans'],
        "ar": ['Amiri', 'Scheherazade', 'DejaVu Sans'],
        "sk": ['DejaVu Sans'],
        "fr": ['DejaVu Sans'],
        "it": ['DejaVu Sans'],
        "pt": ['DejaVu Sans'],
        "default": ['DejaVu Sans']
    }

    lista_fuentes = fuentes_por_idioma.get(idioma, fuentes_por_idioma["default"])

    # Solo usamos fuentes que estén realmente instaladas
    fuentes_validas = [f for f in lista_fuentes if fm.findfont(f, fallback_to_default=False)]
    if not fuentes_validas:
        fuentes_validas = ['DejaVu Sans']

    # Configuración global de matplotlib
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = fuentes_validas
    plt.rcParams['axes.unicode_minus'] = False

    # Configuración de MathText para superíndices, subíndices y símbolos
    rcParams['mathtext.fontset'] = 'dejavusans'
    rcParams['mathtext.rm'] = 'DejaVu Sans'
    rcParams['mathtext.it'] = 'DejaVu Sans:italic'
    rcParams['mathtext.bf'] = 'DejaVu Sans:bold'

    print(f"🔠 Fuente configurada para '{idioma}': {fuentes_validas}")
