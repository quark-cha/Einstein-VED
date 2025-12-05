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

# graficas_einstein_ved_n4.py
import matplotlib.pyplot as plt
import numpy as np
import textwrap
from matplotlib.patches import Circle
import matplotlib.gridspec as gridspec

# --------------------------
# COLORES Y ESTILO
# --------------------------
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16
})

c_MC = "#377eb8"
c_LHC = "#4daf4a"
c_VED = "#e41a1c"
c_BG = "#f0f0f0"

# --------------------------
# DATOS DEL PROTÓN (VALORES EXACTOS)
# --------------------------
MC_mean = 1.00
MC_sigma = 0.30
LHC_mean = 0.84087
LHC_sigma = 0.014
VED_mean = 0.84118
VED_sigma = 0.0  # determinista

# --------------------------
# FUNCIONES GRÁFICAS
# --------------------------

def calcular_rango_3sigma(mean, sigma):
    return mean - 3*sigma, mean, mean + 3*sigma

def crear_grafica_comparativa_proton(filename, y_range, titulo):
    fig, ax = plt.subplots(figsize=(12,7))
    x_positions = [-0.3, 0, 0.3]
    width = 0.15

    # Barras ±3σ
    ax.fill_between([x_positions[0]-width, x_positions[0]+width],
                    MC_mean-3*MC_sigma, MC_mean+3*MC_sigma,
                    color=c_MC, alpha=0.3, label='Modelo Convencional ±3σ')
    
    ax.fill_between([x_positions[1]-width, x_positions[1]+width],
                    LHC_mean-LHC_sigma, LHC_mean+LHC_sigma,
                    color=c_LHC, alpha=0.4, label='LHC Experimental ±3σ')

    # VED determinista
    ax.hlines(VED_mean, x_positions[2]-width, x_positions[2]+width,
              colors=c_VED, linestyles='-', linewidth=3, label='Einstein-VED Determinista')

    # Puntos medios
    ax.scatter(x_positions, [MC_mean, LHC_mean, VED_mean], 
               color=[c_MC, c_LHC, c_VED], s=100, zorder=5)

    # Ejes y etiquetas
    ax.set_ylim(y_range[0], y_range[1])
    ax.set_xlim(-0.7, 0.7)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(['Modelo Convencional', 'LHC Experimental', 'Einstein-VED (n=4)'])
    ax.set_ylabel('Radio del Protón (fm)')
    ax.set_title(titulo, pad=20, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(filename, format='svg', bbox_inches='tight', dpi=300)
    plt.show()
    plt.close()
    print(f"✅ Guardado: {filename}")

def crear_grafica_evolucion_teorica_proton():
    fig, ax = plt.subplots(figsize=(10,6))
    teorias = ['MC Probabilística\n(1920s-)', 'Datos LHC\n(2010s-)', 'Einstein-VED\n(2024-)']
    valores = [MC_mean, LHC_mean, VED_mean]
    incertidumbres = [3*MC_sigma, 3*LHC_sigma, 0.0]
    colores = [c_MC, c_LHC, c_VED]
    
    for i, (t, v, inc, color) in enumerate(zip(teorias, valores, incertidumbres, colores)):
        ax.errorbar(i, v, yerr=inc, fmt='o', color=color, 
                    capsize=8, capthick=2, elinewidth=2, markersize=8,
                    label=t)
    ax.plot(range(len(teorias)), valores, 'k--', alpha=0.5, linewidth=1)
    ax.set_xticks(range(len(teorias)))
    ax.set_xticklabels(teorias)
    ax.set_ylabel('Radio del Protón (fm)')
    ax.set_title('Evolución Teórica: De Probabilidad a Geometría Determinista', 
                 fontweight='bold', pad=20)
    
    ax.annotate('Einstein-VED:\nGeometría exacta\nsin probabilidad', 
                xy=(2, VED_mean), xytext=(1.5, 0.9),
                arrowprops=dict(arrowstyle='->', color=c_VED, lw=2),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffebee"))
    
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('evolucion_teorica_proton.svg', format='svg', bbox_inches='tight', dpi=300)
    plt.show()
    
    plt.close()
    print("✅ Guardado: evolucion_teorica_proton.svg")

def crear_tabla_comparativa_proton():
    fig, ax = plt.subplots(figsize=(10,4))
    ax.axis('tight')
    ax.axis('off')

    column_labels = ['Teoría', 'Radio (fm)', 'Incertidumbre', 'Precisión']
    table_data = [
        ['Einstein-VED (n=4)', f'{VED_mean:.5f}', 'Determinista', '99.96%'],
        ['LHC Experimental', f'{LHC_mean:.5f}', '± 0.014 fm', 'Referencia'],
        ['Modelo Convencional', f'{MC_mean:.2f}', '± 0.90 fm', 'Baja precisión']
    ]

    cell_colors = [
        ['#ffeaea']*4,
        ['#f0f9e8']*4,
        ['#e8f4fd']*4
    ]

    table = ax.table(cellText=table_data, colLabels=column_labels,
                     cellLoc='center', loc='center', cellColours=cell_colors)
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1,1.5)
    for i in range(len(column_labels)):
        table[(0,i)].set_facecolor('#dddddd')
        table[(0,i)].set_text_props(weight='bold')

    plt.title('Comparativa de Radios Protónicos - Datos VED Exactos (n=4)', fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('tabla_comparativa_proton_ved_n4.svg', format='svg', bbox_inches='tight', dpi=300)
    plt.show()
    
    plt.close()
    print("✅ Guardado: tabla_comparativa_proton_ved_n4.svg")

# --------------------------
# NUEVAS GRÁFICAS EINSTEIN-VED
# --------------------------

def crear_grafica_estructuras_atomicas():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,6))
    estados = ['1s','2p','3d','4f']
    radios_ved = [1.0,4.0,9.0,16.0]
    radios_mc = [1.0,4.0,9.0,16.0]
    x_pos = np.arange(len(estados))
    width = 0.35

    ax1.bar(x_pos - width/2, radios_ved, width, label='Einstein-VED', color=c_VED, alpha=0.7)
    ax1.bar(x_pos + width/2, radios_mc, width, label='MC (máximos prob.)', color=c_MC, alpha=0.7)
    ax1.set_xlabel('Estado Cuántico')
    ax1.set_ylabel('Radio (unidades de a₀)')
    ax1.set_title('Radios Atómicos: Valores Exactos vs Probabilísticos', fontweight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(estados)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    for bar in ax1.patches:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height, f'{height:.0f}', ha='center', va='bottom')

    r = np.linspace(0,20,500)
    psi_1s = np.exp(-r)*r**2
    psi_2p = np.exp(-r/2)*r**3
    psi_3d = np.exp(-r/3)*r**4
    psi_1s /= np.max(psi_1s)
    psi_2p /= np.max(psi_2p)
    psi_3d /= np.max(psi_3d)
    ax2.plot(r, psi_1s, label='1s (MC)', color='blue', alpha=0.7)
    ax2.plot(r, psi_2p, label='2p (MC)', color='green', alpha=0.7)
    ax2.plot(r, psi_3d, label='3d (MC)', color='red', alpha=0.7)
    ax2.axvline(x=1, color='blue', linestyle='--', alpha=0.5, label='Radio VED 1s')
    ax2.axvline(x=4, color='green', linestyle='--', alpha=0.5, label='Radio VED 2p')
    ax2.axvline(x=9, color='red', linestyle='--', alpha=0.5, label='Radio VED 3d')
    ax2.set_xlabel('Distancia radial (unidades de a₀)')
    ax2.set_ylabel('Densidad (normalizada)')
    ax2.set_title('Interpretación: Probabilidad MC vs Geometría VED', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0,15)

    plt.tight_layout()
    plt.savefig('estructuras_atomicas_ved.svg', format='svg', bbox_inches='tight', dpi=300)
    plt.show()
    
    plt.close()
    print("✅ Guardado: estructuras_atomicas_ved.svg")

# --------------------------
# MAIN
# --------------------------

if __name__ == "__main__":
    print("🚀 GENERANDO TODAS LAS GRÁFICAS EINSTEIN-VED (n=4)...")
    
    crear_grafica_comparativa_proton("proton_comparativa_ved_n4.svg", [0.75,0.9], "Radio del Protón: Comparativa Exacta Einstein-VED")
    crear_grafica_evolucion_teorica_proton()
    crear_tabla_comparativa_proton()
    crear_grafica_estructuras_atomicas()

    print("🎯 TODAS LAS GRÁFICAS GENERADAS ✅")
