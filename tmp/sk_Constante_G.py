# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Configuración universal para caracteres
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Liberation Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# Nota: Para idiomas específicos, descomenta y ajusta:
# - Chino: plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
# - Japonés: plt.rcParams['font.sans-serif'] = ['IPAexGothic', 'MS Gothic', 'DejaVu Sans']
# - Coreano: plt.rcParams['font.sans-serif'] = ['Malgun Gothic', 'AppleGothic', 'DejaVu Sans']

import numpy as np
import matplotlib.pyplot as plt

# ===========================
# 1. Constantes físicas y datos oficiales (globales)
# ===========================
h = 6.62607015e-34         # J·s
c = 299792458               # m/s
G_exp = 6.67430e-11         # Valor experimental oficial de G
sigma = 1e-14               # Incertidumbre ±3σ aproximada
M_BH = 1.9885e30            # Masa solar ejemplo
n_vals = np.arange(1,6)     # n = 1..5 discretos para VED

# ===========================
# 2. Variables calculadas globales
# ===========================
n_onda = 2
lambda_ = h / (M_BH * c)
L_geom = n_onda * lambda_ / (2*np.pi)

# G(n) según VED
G_calc = [G_exp*(2/n) for n in n_vals]

# Escala hiperlogarítmica
n_hyper = np.linspace(1, 1e6, 1000)
G_hyper = G_exp * (2 / n_hyper)

# Puntos específicos para gráficos
n_puntos = [1,2,3,4,5,6,7,8,30,100,1000,10000,100000,1000000]
G_puntos = [G_exp*(2/n) for n in n_puntos]
colores = ['red' if n==1 else ('green' if n==2 else 'blue') for n in n_puntos]

# ===========================
# 3. Figura 2: Onda confinada VED con detalle protón
# ===========================
theta = np.linspace(0, 2*np.pi, 500)
r = L_geom * np.ones_like(theta)

plt.figure(figsize=(6,6))
ax1 = plt.subplot(111, polar=True)
# Línea media azul discontinua
ax1.plot(theta, r, linestyle='--', color='blue', label='Polomer protónu (stredová čiara)')
# 4 ondas rojas del protón sobre el radio
for k in range(1, n_onda+1):
    ax1.plot(theta, r*(k/n_onda), color='red', linestyle='-', alpha=0.8)
ax1.set_title('Obrázok 1: VED uväznená protónová vlna, n=2', pad=20)
ax1.legend()
plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\SK_figura_1_proton.png", dpi=300)
plt.close()

# ===========================
# 4. Figura 3: Čierna diera y superficie 2D
# ===========================
R_s = 2 * G_exp * M_BH / c**2

plt.figure(figsize=(6,6))
ax2 = plt.gca()
circle = plt.Circle((0,0), R_s, color='black', alpha=0.7, label='Čierna diera')
ax2.add_artist(circle)
circle_surf = plt.Circle((0,0), R_s, color='yellow', fill=False, linewidth=2, label='2D povrch')
ax2.add_artist(circle_surf)
ax2.set_xlim(-R_s*1.2, R_s*1.2)
ax2.set_ylim(-R_s*1.2, R_s*1.2)
ax2.set_aspect('equal', 'box')
plt.title('Figura 2: Čierna diera y superficie 2D holográfica', pad=20)
plt.legend()
plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\SK_figura_2_proton.png", dpi=300)
plt.close()

# ===========================
# 5. Figura 4: Diana de G ±3σ
# ===========================
plt.figure(figsize=(8,6))
colors = ['green' if n==2 else 'blue' for n in n_vals]
plt.fill_between(n_vals, G_exp-3*sigma, G_exp+3*sigma, color='gray', alpha=0.3, label='±3σ')
plt.axhline(G_exp, color='black', linestyle='--', label='Experimentálne G')

for n, G, color in zip(n_vals, G_calc, colors):
    plt.scatter(n, G, color=color, s=100)
    plt.vlines(n, G_exp, G, color=color, linestyle='-', linewidth=2)
    plt.text(n+0.05, G, f'n={n}', fontsize=9)

plt.axvline(2, color='green', linestyle='--', linewidth=1, alpha=0.5)
plt.xlim(0,6)
plt.xlabel('n ∈ Z⁺')
plt.ylabel('Vypočítané G [m^3/kg/s^2]')
plt.title('Obrázok 3: G terč ±3σ', pad=20)
plt.xticks(np.arange(0,6))
plt.grid(True)
plt.legend()
plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\SK_figura_3_G_diana_3sigma.png", dpi=300)
plt.close()

# ===========================
# 6. Figura 5: Diana de G ±4σ con flechas
# ===========================
plt.figure(figsize=(8,6))
plt.fill_between(n_vals, G_exp-4*sigma, G_exp+4*sigma, color='gray', alpha=0.3)
plt.axhline(G_exp, color='black', linestyle='--')

for n, G in zip(n_vals, G_calc):
    if n == 1:
        plt.annotate("↑", (n, G_exp + 4*sigma), ha="center", va="bottom", fontsize=20, color='red')
    elif n == 2:
        plt.scatter(n, G, color='green', s=140, zorder=5)
        plt.vlines(n, G_exp, G, color='green', linestyle='-', linewidth=2)
    else:
        plt.annotate("↓", (n, G_exp - 4*sigma), ha="center", va="top", fontsize=20, color='red')

plt.axvline(2, color='green', linestyle='--', linewidth=1, alpha=0.5)
plt.xlim(0,6)
plt.xlabel('n ∈ Z⁺')
plt.ylabel('Vypočítané G [m^3/kg/s^2]')
plt.title('Obrázok 4: G terč ±4σ (šípky)', pad=20)
plt.xticks(np.arange(0,5))
plt.ylim(G_exp - 6*sigma, G_exp + 6*sigma)
plt.grid(True)
plt.legend()
plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\SK_figura_4_G_diana_4sigma.png", dpi=300)
plt.close()

# ===========================
# 7. Figura 6: Escala hiperlogarítmica n → ∞
# ===========================
plt.figure(figsize=(10,6))
plt.plot(n_hyper, G_hyper, color='purple', label='G(n) asymptotické (spojité)')
plt.scatter(n_puntos, G_puntos, color=colores, s=80, zorder=5)
plt.axvline(2, color='green', linestyle='--', linewidth=2, alpha=0.5)
plt.axhline(G_exp, color='black', linestyle='--', label='Experimentálne G')

plt.xscale('log')
plt.yscale('log')
plt.xticks(n_puntos, labels=[str(n) for n in n_puntos])
plt.text(4, 1e-14, 'n ∈ Z⁺ \nhranica n→∞ G(n)=0',
         fontsize=10, color='black',
         bbox=dict(facecolor='white', alpha=0.7, edgecolor='black', boxstyle='round,pad=0.5'))
plt.xlabel('n')
plt.ylabel('G(n) [m^3/kg/s^2]')
plt.title('Obrázok 5: Asymptotické správanie G(n) n→∞ (log-log)', pad=20)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\SK_figura_5_G_asintotica_log.png", dpi=300)
plt.close()

# ===========================
# 9. Figura 7: Tabla independiente para n=2 con ±3σ - CON RECTÁNGULO
# ===========================
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')

G_n2 = G_calc[1]
G_max = G_exp + 3*sigma
G_min = G_exp - 3*sigma
error_abs = abs(G_n2 - G_exp)
error_rel = 100 * error_abs / G_exp

# Datos de la tabla
tabla_datos = [
    [" Concepto ", " Hodnota [m³/kg·s²] ", " Origen "],
    [r" $G_{MAX}$ +3σ ", f" {G_max:.8e} ", " Horná hranica "],
    [r" $G_2^{EXP}$ Experimentálne ", f" {G_exp:.8e} ", " Priemerná hodnota "], 
    [r" $G_{MIN}$ -3σ ", f" {G_min:.8e} ", " Dolná hranica "],
    [r" $G_1^{VED}$ (n=2) PRESNÉ ", f" {G_n2:.8e} ", " Empiricky získané "],
    [" Absolútny rozdiel ", f" {error_abs:.8e} ", " |G₁ - G₂| "],
    [" Relatívna chyba ", f" {error_rel:.6f} % ", " VED presnosť "]
]

# Crear tabla
tabla = ax.table(cellText=tabla_datos, 
                cellLoc='center', 
                loc='center',
                colWidths=[0.25, 0.4, 0.25])

# Formatear tabla
tabla.auto_set_font_size(False)
tabla.set_fontsize(11)
tabla.scale(1, 1.8)

# Colores
colores_fondo = [
    ['black', 'black', 'black'],           # Encabezado
    ['#F5F5DC', '#F5F5DC', '#F5F5DC'],    # G_MAX
    ['#F5F5DC', '#F5F5DC', '#F5F5DC'],    # G Experimental  
    ['#F5F5DC', '#F5F5DC', '#F5F5DC'],    # G_MIN
    ['#90EE90', '#90EE90', '#90EE90'],    # G VED - EXACTO
    ['#E6E6FA', '#E6E6FA', '#E6E6FA'],    # Diferencia
    ['#FFB6C1', '#FFB6C1', '#FFB6C1']     # Error
]

colores_texto = [
    ['white', 'white', 'white'],           # Encabezado
    ['#8B8000', '#8B8000', '#8B8000'],    # G_MAX
    ['#8B8000', '#8B8000', '#8B8000'],    # G Experimental
    ['#8B8000', '#8B8000', '#8B8000'],    # G_MIN
    ['#006400', '#006400', '#006400'],    # G VED
    ['#4B0082', '#4B0082', '#4B0082'],    # Diferencia
    ['#8B0000', '#8B0000', '#8B0000']     # Error
]

# Aplicar estilos a las celdas
for (i, j), cell in tabla.get_celld().items():
    if i == 0:  # Encabezado
        cell.set_facecolor(colores_fondo[i][j])
        cell.set_text_props(weight='bold', color=colores_texto[i][j], fontsize=12)
    else:
        cell.set_facecolor(colores_fondo[i][j])
        if i == 4:  # G1 VED - VALOR EXACTO
            cell.set_text_props(weight='bold', color=colores_texto[i][j], fontsize=12)
        elif i in [1, 2, 3]:  # Filas experimentales
            cell.set_text_props(weight='bold', color=colores_texto[i][j], fontsize=11)
        else:
            cell.set_text_props(weight='normal', color=colores_texto[i][j], fontsize=11)
    cell.set_edgecolor('white')
    cell.set_linewidth(2)
    cell.set_height(0.12)

# RECTÁNGULO ALREDEDOR DE LA FILA EXPERIMENTAL
from matplotlib.patches import Rectangle

# Forzar el dibujo para calcular coordenadas
fig.canvas.draw()

# Obtener las celdas de la fila experimental (fila 2)
cell_left = tabla.get_celld()[(2,0)]
cell_right = tabla.get_celld()[(2,2)]

# Obtener las bounding boxes transformadas
bbox_left = cell_left.get_window_extent().transformed(fig.transFigure.inverted())
bbox_right = cell_right.get_window_extent().transformed(fig.transFigure.inverted())

# Calcular posición y tamaño del rectángulo
x = bbox_left.x0
y = bbox_left.y0 
width = bbox_right.x1 - bbox_left.x0
height = bbox_left.y1 - bbox_left.y0






plt.title("GRAVITAČNÁ KONŠTANTA G", 
          fontsize=16, pad=20, weight='bold')

plt.tight_layout()
plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\SK_figura_7_tabla_n2.png", dpi=300, bbox_inches='tight')
plt.close()

# ===========================
# 10. Figura 7: Conceptual – Materia como onda confinada sobre un holograma
# ===========================
plt.figure(figsize=(8,8))
ax = plt.subplot(111, polar=True)

# Onda confinada (como en Figura 1)
theta = np.linspace(0, 2*np.pi, 500)
r = L_geom * np.ones_like(theta)

# Texto posicionado a 90 grados
ax.text(np.pi/2, r[0]*0.7, 'Uväznená hmotová vlna', color='blue', fontsize=12, 
        ha='center', va='center', weight='bold')

for k in range(1, n_onda+1):
    ax.plot(theta, r*(k/n_onda), linestyle='--', alpha=0.5)

# Añadir "holograma" 2D conceptual
circle_holo = plt.Circle((0,0), L_geom*1.2, transform=ax.transData._b, color='orange', fill=False, linewidth=2, linestyle=':')
ax.add_artist(circle_holo)

ax.text(5*np.pi/4, L_geom*0.4, '2D hologram', color='orange', fontsize=12, 
        ha='center', va='center', rotation=45, rotation_mode='anchor')

# Flechas que muestran emergencia de G
arrow_r = L_geom*1.4
arrow_angles = [np.pi/6, np.pi/3, np.pi/2, 2*np.pi/3]
for angle in arrow_angles:
    ax.annotate('', xy=(angle, arrow_r), xytext=(angle, arrow_r+L_geom*0.3),
                arrowprops=dict(facecolor='green', shrink=0.05, width=3, headwidth=8))
ax.text(np.pi/2, arrow_r+L_geom*0.35, 'Vynorenie G', color='green', fontsize=12, ha='center')

ax.set_title('Obrázok 8: Hmota ako uväznená vlna na 2D holograme', fontsize=14, pad=20)
ax.legend(loc='upper right', fontsize=10)
plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\SK_figura_8_materia_holograma.png", dpi=300)
plt.close()

# ============================
# 11. FIGURA 9 — PROTÓN Y ELECTRÓN CON DOS ESCALAS SEPARADAS
# ============================

# DEFINIR LAS VARIABLES CON TUS VALORES EXACTOS
r_p = 0.84118e-15  # Polomer protónu exacto
r_e = 5.29177210903e-11  # Radio de Bohr

theta = np.linspace(0, 2 * np.pi, 2000)

# Crear figura con dos subplots
fig9, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), subplot_kw=dict(projection='polar'))

# ============================================
# PANEL IZQUIERDO: PROTÓN (escala femtométrica)
# ============================================

# Líneas medias protón
r_proton = np.full_like(theta, r_p)
ondas_proton = r_p + 0.1 * r_p * np.sin(4 * theta)
onda2d_proton = r_p + 0.01 * r_p * np.sin(4 * theta)

# Protón
ax1.plot(theta, r_proton, '--', color='blue', linewidth=2, label='Polomer protónu')
ax1.plot(theta, ondas_proton, color='red', linewidth=1.5, label='Radiálne protónové vlny')
ax1.plot(theta, onda2d_proton, color='darkred', linewidth=2, alpha=0.8, label='2D protónová vlnovitosť (n=4)')

# Etiquetas protón
ax1.text(np.pi/2, r_p * 1.3, 'Polomer protónu', color='blue', ha='center', va='center', fontsize=11, weight='bold')
ax1.text(0, r_p * 1.1, 'Protónové vlny', color='red', ha='center', va='center', fontsize=10)
ax1.text(np.pi, r_p * 1.15, '2D vlnovitosť', color='darkred', ha='center', va='center', fontsize=9)

ax1.set_title("Protón - Femtometrová mierka (10⁻¹⁵ m)", fontsize=12, pad=20)
ax1.set_rticks([])
ax1.grid(False)
ax1.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
ax1.set_ylim(0, r_p * 1.5)

# ============================================
# PANEL DERECHO: ELECTRÓN (escala atómica)
# ============================================

# Líneas medias electrón
r_electron = np.full_like(theta, r_e)
ondas_electron = r_e + 0.03 * r_e * np.sin(137 * theta)
onda2d_electron = r_e + 0.005 * r_e * np.sin(137 * theta)

# Electrón
ax2.plot(theta, r_electron, '--', color='green', linewidth=2, label='Polomer elektrónového orbitálu')
ax2.plot(theta, ondas_electron, color='magenta', linewidth=1.3, label='Radiálne elektrónové vlny')
ax2.plot(theta, onda2d_electron, color='purple', linewidth=1.8, alpha=0.8, label='2D vlnovitosť electrón (n=137)')

# Etiquetas electrón
ax2.text(np.pi/2, r_e * 1.1, 'Polomer elektrónového orbitálu', color='green', ha='center', va='center', fontsize=11, weight='bold')
ax2.text(0, r_e * 0.6, 'Elektrónové vlny', color='magenta', ha='center', va='center', fontsize=10)
ax2.text(np.pi, r_e * 0.7, '2D vlnovitosť', color='purple', ha='center', va='center', fontsize=9)

ax2.set_title("Elektrón - Atómová mierka (10⁻¹¹ m)", fontsize=12, pad=20)
ax2.set_rticks([])
ax2.grid(False)
ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
ax2.set_ylim(0, r_e * 1.2)

# Título principal
plt.suptitle("Obrázok 9. 2D a radiálne vlny protónu a elektrónu\n(holografia → častice)", 
             fontsize=16, y=0.95)

plt.tight_layout(pad=3.0)

plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\SK_figura_9_proton_electron.png", dpi=300, bbox_inches='tight')



# ===========================
# 12. Figura 1: Tabla conceptual VED vs Schwarzschild
# ===========================
plt.figure(figsize=(14, 6))  # Aumentado el ancho
ax10 = plt.gca()
ax10.axis('off')

# Datos de la tabla con textos en dos líneas
tabla_datos = [
    ['Concepto', 'VED', 'Schwarzschild', 'Comentario'],
    ['Masa', r'$M_\mathrm{VED} = n h /$' + '\n' + r'$(L_\mathrm{geom} c)$', 
     r'$M_\mathrm{Sch} = c^2 R_s /$' + '\n' + r'$(2 G)$', 'Rovnanie hmotností,\nM zmizne'],
    ['Longitud', r'$L_\mathrm{geom}$ definovaná' + '\n' + 'VED', 
     r'$R_s$ definovaná' + '\n' + 'Schwarzschild', 'Každá strana definuje\nvlastnú mierku'],
    ['Kvantovanie', 'n celé → hodnoty' + '\n' + 'diskrétne hodnoty M a G', 
     'n sa neobjavuje,\nG je určené', 'n=2 sa zhoduje s\nexperimentálnou hodnotou G'],
    ['Dimensionalidad', '2D uväznenie' + '\n' + '(povrch)', 
     '3D → holografia' + '\n' + 'implicitná', 'Vznikajúci pôvod\ngravitácie']
]

# Crear tabla
tabla = ax10.table(cellText=tabla_datos, 
                   loc='center', 
                   cellLoc='center',  # Cambiado a center para mejor visualización
                   colWidths=[0.15, 0.25, 0.25, 0.35])

# Formatear tabla
tabla.auto_set_font_size(False)
tabla.set_fontsize(12)  # Reducido ligeramente el tamaño de fuente
tabla.scale(1, 1.8)    # Ajustada la escala

# Estilo de celdas
for (i, j), cell in tabla.get_celld().items():
    if i == 0:  # Encabezado
        cell.set_facecolor('#4CAF50')
        cell.set_text_props(weight='bold', color='white')
    else:
        cell.set_facecolor('#f5f5f5')
    cell.set_edgecolor('black')
    cell.set_height(0.2)  # Aumentada la altura de celdas

plt.title('Obrázok 10: Konceptuálne porovnanie VED vs Schwarzschild', fontsize=14, pad=25)
plt.tight_layout()
plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\SK_figura_10_tabla_conceptual.png", dpi=300, bbox_inches='tight')
plt.close()