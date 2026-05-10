import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as fm

def configurar_fuentes(idioma, plt=None):
    """
    Configura la fuente de matplotlib según el idioma.
    Usa DejaVu Sans como fallback si no se encuentra la fuente principal.
    """
    fuentes_por_idioma = {
        "ja": ['Yu Gothic', 'Meiryo', 'MS Gothic', 'MS Mincho', 'DejaVu Sans'],
        "zh": ['SimHei', 'Microsoft YaHei', 'SimSun', 'DejaVu Sans'],
        "ar": ['Amiri', 'Scheherazade', 'DejaVu Sans'],
        "sk": ['DejaVu Sans'],
        "fr": ['DejaVu Sans'],
        "it": ['DejaVu Sans'],
        "pt": ['DejaVu Sans'],
        "default": ['DejaVu Sans']
    }

    lista_fuentes = fuentes_por_idioma.get(idioma, fuentes_por_idioma["default"])

    # Solo usamos fuentes que estén realmente instaladas

    try:
        fuentes_validas = []
        for f in lista_fuentes:
            try:
                fm.findfont(f, fallback_to_default=False)
                fuentes_validas.append(f)
            except Exception:
                # La fuente no está disponible, se ignora
                pass

        # Si ninguna fuente válida fue encontrada, usar fallback seguro
        if not fuentes_validas:
            fuentes_validas = ['DejaVu Sans']

    except Exception:
        # Fallback absoluto: nunca fallar
        fuentes_validas = ['DejaVu Sans']

    # ===========================
    # Configuración global de matplotlib
    # ===========================
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = fuentes_validas
    plt.rcParams['axes.unicode_minus'] = False

    # ===========================
    # Configuración de MathText (SIEMPRE estable)
    # ===========================
    rcParams['mathtext.fontset'] = 'dejavusans'
    rcParams['mathtext.rm'] = 'DejaVu Sans'
    rcParams['mathtext.it'] = 'DejaVu Sans:italic'
    rcParams['mathtext.bf'] = 'DejaVu Sans:bold'

    print(f"🔠 Fuente configurada para '{idioma}': {fuentes_validas}")
