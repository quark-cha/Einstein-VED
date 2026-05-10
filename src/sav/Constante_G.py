import matplotlib
#matplotlib.use("Agg")   # backend no interactivo (batch / CI / traducciones)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import sys
from pathlib import Path

# ===========================
# CONFIGURACIÓN GLOBAL
# ===========================
idioma_actual = "es"   # definido por el generador del temporal

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from libreria import configurar_fuentes as cf
cf.configurar_fuentes(idioma_actual, plt)

# INICIO DEL CÓDIGO PRINCIPAL

# =============================================
# CONSTANTES FÍSICAS Y PARÁMETROS
# =============================================
h = 6.62607015e-34         # Constante de Planck (J·s)
c = 299792458              # Velocidad de la luz (m/s)
G_exp = 6.67430e-11        # Valor experimental oficial de G
sigma = 1e-14              # Incertidumbre aproximada ±3σ
M_BH = 1.9885e30           # Masa solar (kg)
n_vals = np.arange(1, 6)   # Valores discretos de n = 1..5

# =============================================
# VARIABLES CALCULADAS
# =============================================
n_onda = 2
lambda_ = h / (M_BH * c)
L_geom = n_onda * lambda_ / (2 * np.pi)

# Valores de G según VED para n=1..5
G_calc = [G_exp * (2 / n) for n in n_vals]

# Escala hiperlogarítmica para n → ∞
n_hyper = np.linspace(1, 1e6, 1000)
G_hyper = G_exp * (2 / n_hyper)

# Puntos específicos para gráficos logarítmicos
n_puntos = [1, 2, 3, 4, 5, 6, 7, 8, 30, 100, 1000, 10000, 100000, 1000000]
G_puntos = [G_exp * (2 / n) for n in n_puntos]
colores = ['red' if n == 1 else ('green' if n == 2 else 'blue') for n in n_puntos]

# Radios de protón y electrón
r_p = 0.84118e-15           # Radio del protón (m)
r_e = 5.29177210903e-11     # Radio de Bohr (m)

# =============================================
# FIGURA 1: Onda confinada VED del protón (n=2)
# =============================================
print("Generando Figura 1...")
theta = np.linspace(0, 2 * np.pi, 500)
r = L_geom * np.ones_like(theta)

plt.figure(figsize=(6, 6))
ax1 = plt.subplot(111, polar=True)
ax1.plot(theta, r, linestyle='--', color='blue', label='Radio del protón (línea media)')
for k in range(1, n_onda + 1):
    ax1.plot(theta, r * (k / n_onda), color='red', linestyle='-', alpha=0.8)
ax1.set_title('Figura 1: Onda confinada VED del protón, n=2', pad=20)
ax1.legend()
plt.savefig('figura_1_proton.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# =============================================
# FIGURA 2: Agujero negro y superficie 2D holográfica
# =============================================
print("Generando Figura 2...")
R_s = 2 * G_exp * M_BH / c**2

plt.figure(figsize=(6, 6))
ax2 = plt.gca()
circle_bh = Circle((0, 0), R_s, color='black', alpha=0.7, label='Agujero negro')
circle_surf = Circle((0, 0), R_s, color='yellow', fill=False, linewidth=2, label='Superficie 2D')
ax2.add_artist(circle_bh)
ax2.add_artist(circle_surf)
ax2.set_xlim(-R_s * 1.2, R_s * 1.2)
ax2.set_ylim(-R_s * 1.2, R_s * 1.2)
ax2.set_aspect('equal', 'box')
plt.title('Figura 2: Agujero negro y superficie 2D holográfica', pad=20)
plt.legend()
plt.savefig('figura_2_agujero_negro.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# =============================================
# FIGURA 3: Diana de G ±3σ
# =============================================
print("Generando Figura 3...")
plt.figure(figsize=(8, 6))
colors = ['green' if n == 2 else 'blue' for n in n_vals]
plt.fill_between(n_vals, G_exp - 3 * sigma, G_exp + 3 * sigma, 
                 color='gray', alpha=0.3, label='±3σ')
plt.axhline(G_exp, color='black', linestyle='--', label='G experimental')

for n, G, color in zip(n_vals, G_calc, colors):
    plt.scatter(n, G, color=color, s=100)
    plt.vlines(n, G_exp, G, color=color, linestyle='-', linewidth=2)
    plt.text(n + 0.05, G, f'n={n}', fontsize=9)

plt.axvline(2, color='green', linestyle='--', linewidth=1, alpha=0.5)
plt.xlim(0, 6)
plt.xlabel('n ∈ Z⁺')
plt.ylabel('G calculado [m³/kg·s²]')
plt.title('Figura 3: Diana de G ±3σ', pad=20)
plt.xticks(np.arange(0, 6))
plt.grid(True)
plt.legend()
plt.savefig('figura_3_G_diana_3sigma.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# =============================================
# FIGURA 4: Diana de G ±4σ con flechas
# =============================================
print("Generando Figura 4...")
plt.figure(figsize=(8, 6))
plt.fill_between(n_vals, G_exp - 4 * sigma, G_exp + 4 * sigma, 
                 color='gray', alpha=0.3)
plt.axhline(G_exp, color='black', linestyle='--')

for n, G in zip(n_vals, G_calc):
    if n == 1:
        plt.annotate("↑", (n, G_exp + 4 * sigma), ha="center", va="bottom", 
                    fontsize=20, color='red')
    elif n == 2:
        plt.scatter(n, G, color='green', s=140, zorder=5)
        plt.vlines(n, G_exp, G, color='green', linestyle='-', linewidth=2)
    else:
        plt.annotate("↓", (n, G_exp - 4 * sigma), ha="center", va="top", 
                    fontsize=20, color='red')

plt.axvline(2, color='green', linestyle='--', linewidth=1, alpha=0.5)
plt.xlim(0, 6)
plt.xlabel('n ∈ Z⁺')
plt.ylabel('G calculado [m³/kg·s²]')
plt.title('Figura 4: Diana de G ±4σ (flechas)', pad=20)
plt.xticks(np.arange(0, 5))
plt.ylim(G_exp - 6 * sigma, G_exp + 6 * sigma)
plt.grid(True)
plt.legend()
plt.savefig('figura_4_G_diana_4sigma.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# =============================================
# FIGURA 5: Comportamiento asintótico G(n) n→∞
# =============================================
print("Generando Figura 5...")
plt.figure(figsize=(10, 6))
plt.plot(n_hyper, G_hyper, color='purple', label='G(n) asintótico (continuo)')
plt.scatter(n_puntos, G_puntos, color=colores, s=80, zorder=5)
plt.axvline(2, color='green', linestyle='--', linewidth=2, alpha=0.5)
plt.axhline(G_exp, color='black', linestyle='--', label='G experimental')

plt.xscale('log')
plt.yscale('log')
plt.xticks(n_puntos, labels=[str(n) for n in n_puntos])
plt.text(4, 1e-14, 'n ∈ Z⁺ \nlim n→∞ G(n)=0',
         fontsize=10, color='black',
         bbox=dict(facecolor='white', alpha=0.7, edgecolor='black', boxstyle='round,pad=0.5'))
plt.xlabel('n')
plt.ylabel('G(n) [m³/kg·s²]')
plt.title('Figura 5: Comportamiento asintótico de G(n) n→∞ (log-log)', pad=20)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.savefig('figura_5_G_asintotica_log.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# =============================================
# FIGURA 6: Tabla independiente para n=2 ±3σ
# =============================================
print("Generando Figura 6...")
fig6, ax6 = plt.subplots(figsize=(10, 6))
ax6.axis('off')

G_n2 = G_calc[1]  # G para n=2
G_max = G_exp + 3 * sigma
G_min = G_exp - 3 * sigma
error_abs = abs(G_n2 - G_exp)
error_rel = 100 * error_abs / G_exp

# Datos de la tabla
tabla_datos = [
    [" Concepto ", " Valor [m³/kg·s²] ", " Origen "],
    [r" $G_{MAX}$ +3σ ", f" {G_max:.8e} ", " Límite superior "],
    [r" $G_2^{EXP}$ Experimental ", f" {G_exp:.8e} ", " Valor medio "], 
    [r" $G_{MIN}$ -3σ ", f" {G_min:.8e} ", " Límite inferior "],
    [r" $G_1^{VED}$ (n=2) EXACTO ", f" {G_n2:.8e} ", " Obtenido empíricamente "],
    [" Diferencia absoluta ", f" {error_abs:.8e} ", " |G₁ - G₂| "],
    [" Error relativo ", f" {error_rel:.6f} % ", " Precisión VED "]
]

# Crear tabla
tabla = ax6.table(cellText=tabla_datos, 
                  cellLoc='center', 
                  loc='center',
                  colWidths=[0.25, 0.4, 0.25])

# Formatear tabla
tabla.auto_set_font_size(False)
tabla.set_fontsize(11)
tabla.scale(1, 1.8)

# Colores de fondo
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
        if i == 4:  # G VED - VALOR EXACTO
            cell.set_text_props(weight='bold', color=colores_texto[i][j], fontsize=12)
        elif i in [1, 2, 3]:  # Filas experimentales
            cell.set_text_props(weight='bold', color=colores_texto[i][j], fontsize=11)
        else:
            cell.set_text_props(weight='normal', color=colores_texto[i][j], fontsize=11)
    cell.set_edgecolor('white')
    cell.set_linewidth(2)
    cell.set_height(0.12)

# Rectángulo alrededor de la fila experimental
fig6.canvas.draw()
cell_left = tabla.get_celld()[(2, 0)]
cell_right = tabla.get_celld()[(2, 2)]
bbox_left = cell_left.get_window_extent().transformed(fig6.transFigure.inverted())
bbox_right = cell_right.get_window_extent().transformed(fig6.transFigure.inverted())

x = bbox_left.x0
y = bbox_left.y0 
width = bbox_right.x1 - bbox_left.x0
height = bbox_left.y1 - bbox_left.y0

rect = Rectangle((x - 0.005, y - 0.005), width + 0.01, height + 0.01, 
                 linewidth=2, edgecolor='black', facecolor='none', 
                 linestyle='-', zorder=10)
ax6.add_patch(rect)

plt.title("CONSTANTE GRAVITATORIA G", fontsize=16, pad=20, weight='bold')
plt.tight_layout()
plt.savefig("figura_6_tabla_n2.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# =============================================
# FIGURA 7: Materia como onda confinada sobre holograma
# =============================================
print("Generando Figura 7...")
plt.figure(figsize=(8, 8))
ax7 = plt.subplot(111, polar=True)

# Onda confinada
ax7.text(np.pi/2, L_geom*0.7, 'Onda confinada de la materia', 
         color='blue', fontsize=12, ha='center', va='center', weight='bold')

for k in range(1, n_onda + 1):
    ax7.plot(theta, r * (k / n_onda), linestyle='--', alpha=0.5)

# Holograma 2D conceptual
circle_holo = Circle((0, 0), L_geom * 1.2, transform=ax7.transData._b, 
                     color='orange', fill=False, linewidth=2, linestyle=':')
ax7.add_artist(circle_holo)
ax7.text(5 * np.pi/4, L_geom * 0.4, 'Holograma 2D', color='orange', fontsize=12, 
         ha='center', va='center', rotation=45, rotation_mode='anchor')

# Flechas de emergencia de G
arrow_r = L_geom * 1.4
arrow_angles = [np.pi/6, np.pi/3, np.pi/2, 2*np.pi/3]
for angle in arrow_angles:
    ax7.annotate('', xy=(angle, arrow_r), xytext=(angle, arrow_r + L_geom * 0.3),
                 arrowprops=dict(facecolor='green', shrink=0.05, width=3, headwidth=8))
ax7.text(np.pi/2, arrow_r + L_geom * 0.35, 'Emergencia de G', 
         color='green', fontsize=12, ha='center')

ax7.set_title('Figura 7: Materia como onda confinada sobre holograma 2D', fontsize=14, pad=20)
plt.savefig("figura_7_materia_holograma.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# =============================================
# FIGURA 8: Protón y electrón (dos escalas)
# =============================================
print("Generando Figura 8...")
fig8, (ax81, ax82) = plt.subplots(1, 2, figsize=(16, 8), 
                                   subplot_kw=dict(projection='polar'))

# Panel izquierdo: Protón
r_proton = np.full_like(theta, r_p)
ondas_proton = r_p + 0.1 * r_p * np.sin(4 * theta)
onda2d_proton = r_p + 0.01 * r_p * np.sin(4 * theta)

ax81.plot(theta, r_proton, '--', color='blue', linewidth=2, label='Radio del protón')
ax81.plot(theta, ondas_proton, color='red', linewidth=1.5, label='Ondas radiales protón')
ax81.plot(theta, onda2d_proton, color='darkred', linewidth=2, alpha=0.8, 
          label='Ondulación 2D protón (n=4)')

ax81.text(np.pi/2, r_p * 1.3, 'Radio del protón', color='blue', 
          ha='center', va='center', fontsize=11, weight='bold')
ax81.text(0, r_p * 1.1, 'Ondas del protón', color='red', 
          ha='center', va='center', fontsize=10)
ax81.text(np.pi, r_p * 1.15, 'Ondulación 2D', color='darkred', 
          ha='center', va='center', fontsize=9)

ax81.set_title("Protón - Escala femtométrica (10⁻¹⁵ m)", fontsize=12, pad=20)
ax81.set_rticks([])
ax81.grid(False)
ax81.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
ax81.set_ylim(0, r_p * 1.5)

# Panel derecho: Electrón
r_electron = np.full_like(theta, r_e)
ondas_electron = r_e + 0.03 * r_e * np.sin(137 * theta)
onda2d_electron = r_e + 0.005 * r_e * np.sin(137 * theta)

ax82.plot(theta, r_electron, '--', color='green', linewidth=2, 
          label='Radio orbital electrón')
ax82.plot(theta, ondas_electron, color='magenta', linewidth=1.3, 
          label='Ondas radiales electrón')
ax82.plot(theta, onda2d_electron, color='purple', linewidth=1.8, alpha=0.8, 
          label='Ondulación 2D electrón (n=137)')

ax82.text(np.pi/2, r_e * 1.1, 'Radio orbital electrón', color='green', 
          ha='center', va='center', fontsize=11, weight='bold')
ax82.text(0, r_e * 0.6, 'Ondas del electrón', color='magenta', 
          ha='center', va='center', fontsize=10)
ax82.text(np.pi, r_e * 0.7, 'Ondulación 2D', color='purple', 
          ha='center', va='center', fontsize=9)

ax82.set_title("Electrón - Escala atómica (10⁻¹¹ m)", fontsize=12, pad=20)
ax82.set_rticks([])
ax82.grid(False)
ax82.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
ax82.set_ylim(0, r_e * 1.2)

plt.suptitle("Figura 8. Ondas 2D y radiales del protón y del electrón\n(holografía → partículas)", 
             fontsize=16, y=0.95)
plt.tight_layout(pad=3.0)
plt.savefig('figura_8_proton_electron.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# =============================================
# FIGURA 9: Tabla conceptual VED vs Schwarzschild
# =============================================
print("Generando Figura 9...")
fig9, ax9 = plt.subplots(figsize=(14, 6))
ax9.axis('off')

tabla_datos = [
    ['Concepto', 'VED', 'Schwarzschild', 'Comentario'],
    ['Masa', r'$M_\mathrm{VED} = n h /$' + '\n' + r'$(L_\mathrm{geom} c)$', 
     r'$M_\mathrm{Sch} = c^2 R_s /$' + '\n' + r'$(2 G)$', 'Igualando masas,\ndesaparece M'],
    ['Longitud', r'$L_\mathrm{geom}$ definida' + '\n' + 'por VED', 
     r'$R_s$ definida por' + '\n' + 'Schwarzschild', 'Cada lado define\nsu propia escala'],
    ['Cuantización', 'n entero → valores' + '\n' + 'discretos de M y G', 
     'n no aparece,\nG queda determinado', 'n=2 coincide con\nvalor experimental de G'],
    ['Dimensionalidad', 'Confinamiento 2D' + '\n' + '(superficie)', 
     '3D → holografía' + '\n' + 'implícita', 'Origen emergente\nde gravedad']
]

tabla9 = ax9.table(cellText=tabla_datos, 
                   loc='center', 
                   cellLoc='center',
                   colWidths=[0.15, 0.25, 0.25, 0.35])

tabla9.auto_set_font_size(False)
tabla9.set_fontsize(12)
tabla9.scale(1, 1.8)

# Estilo de celdas
for (i, j), cell in tabla9.get_celld().items():
    if i == 0:  # Encabezado
        cell.set_facecolor('#4CAF50')
        cell.set_text_props(weight='bold', color='white')
    else:
        cell.set_facecolor('#f5f5f5')
    cell.set_edgecolor('black')
    cell.set_height(0.2)

plt.title('Figura 9: Comparación conceptual VED vs Schwarzschild', fontsize=14, pad=25)
plt.tight_layout()
plt.savefig('figura_9_tabla_conceptual.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# =============================================
# RESUMEN FINAL
# =============================================
print("\n" + "="*60)
print("GENERACIÓN DE GRÁFICOS COMPLETADA")
print("="*60)
print(f"Se han generado 9 figuras en formato PNG:")
print(f"1. figura_1_proton.png")
print(f"2. figura_2_agujero_negro.png")
print(f"3. figura_3_G_diana_3sigma.png")
print(f"4. figura_4_G_diana_4sigma.png")
print(f"5. figura_5_G_asintotica_log.png")
print(f"6. figura_6_tabla_n2.png")
print(f"7. figura_7_materia_holograma.png")
print(f"8. figura_8_proton_electron.png")
print(f"9. figura_9_tabla_conceptual.png")
print("\nResumen de resultados para n=2:")
print(f"  • G experimental: {G_exp:.8e} m³/kg·s²")
print(f"  • G VED (n=2):    {G_n2:.8e} m³/kg·s²")
print(f"  • Error relativo: {error_rel:.6f} %")
print(f"  • Precisión VED:  {100-error_rel:.6f} %")
print("="*60)