import matplotlib.pyplot as plt
import numpy as np
import textwrap

# --------------------------
# VALORES PARA GRÁFICAS DEL PROTÓN
# --------------------------
MC_mean = 1.00
MC_sigma = 0.30     # ±3σ probabilistic uncertainty
LHC_mean = 0.84087
LHC_sigma = 0.014
VED_mean = 0.84118
VED_sigma = 0.00031  # derivada de la masa conocida

c_MC = "#377eb8"
c_LHC = "#4daf4a"
c_VED = "#e41a1c"
c_BG = "#f0f0f0"

def calcular_rango_3sigma(mean, sigma):
    """Calcula rango ±3σ para visualización"""
    return mean - 3*sigma, mean, mean + 3*sigma


def crear_grafica_doble_escala_corregida():
    fig, ax = plt.subplots(figsize=(10,6))
    fig.patch.set_facecolor(c_BG)
    ax.set_facecolor('white')

    # Rangos ±3σ
    mc_min, mc_mean, mc_max = calcular_rango_3sigma(MC_mean, MC_sigma)
    lhc_min, lhc_mean, lhc_max = calcular_rango_3sigma(LHC_mean, LHC_sigma)
    ved_min, ved_mean, ved_max = calcular_rango_3sigma(VED_mean, VED_sigma)

    mc_min, mc_mean, mc_max = calcular_rango_3sigma(MC_mean, MC_sigma)
    lhc_min, lhc_mean, lhc_max = calcular_rango_3sigma(LHC_mean, LHC_sigma)
    ved_min, ved_mean, ved_max = calcular_rango_3sigma(VED_mean, VED_sigma)    

    # Posiciones x y ancho de barras
    x_positions = [0, 1, 2]
    width = 0.3

    # --- BARRAS DE INCERTIDUMBRE ---
    ax.fill_between([x_positions[0]-width, x_positions[0]+width], mc_min, mc_max,
                    color=c_MC, alpha=0.3, label='MC: Probabilistic')
    ax.fill_between([x_positions[1]-width, x_positions[1]+width], lhc_min, lhc_max,
                    color=c_LHC, alpha=0.4, label='LHC: Experimental')
    ax.fill_between([x_positions[2]-width, x_positions[2]+width], ved_min, ved_max,
                    color=c_VED, alpha=0.6, label='Einstein-VED: Deterministic')

    # --- LÍNEAS DE VALORES MEDIOS ---
    ax.hlines(mc_mean, x_positions[0]-width, x_positions[0]+width, colors=c_MC, linestyles='--', lw=2)
    ax.hlines(lhc_mean, x_positions[1]-width, x_positions[1]+width, colors=c_LHC, linestyles='--', lw=2)
    ax.hlines(ved_mean, x_positions[2]-width, x_positions[2]+width, colors=c_VED, linestyles='-', lw=3)

    # --- PUNTOS ---
    ax.scatter(x_positions, [mc_mean, lhc_mean, ved_mean], color=[c_MC, c_LHC, c_VED],
               s=120, zorder=5, edgecolors='black', linewidth=1)

    # --- CONFIGURACIÓN ---
    ax.set_xticks(x_positions)
    ax.set_xticklabels(['Quantum Mechanics', 'LHC Experimental', 'Einstein-VED'], rotation=15)
    ax.set_ylabel('Proton Radius (fm)', fontweight='bold')
    ax.set_title('Proton Radius Estimates\nwith ±3σ Ranges', fontweight='bold', fontsize=14)

    # Escala ajustada para mostrar comparativa MC vs LHC/Einstein-VED
    ax.set_ylim(0.6, 1.05)
    ax.set_xlim(-0.5, 2.5)
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

    # --- LEYENDA ---
    ax.legend(loc='upper right', framealpha=0.9)

    # --- CUADRO EXPLICATIVO EINSTEIN-VED ---
    texto_ved = textwrap.fill(
        "Einstein-VED: Deterministic geometric model of proton. "
        "Radius derived from 4 wavelengths of confinement.", width=40
    )
    ax.text(0.6, 0.2, texto_ved, transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffebee", alpha=0.9,
                      edgecolor=c_VED, linewidth=2), verticalalignment='top', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig('proton_doble_escala_corregida.svg', format='svg', dpi=300)
    
    plt.show()

    plt.close()
    print("✅ Guardado: proton_doble_escala_corregida.svg")

# -----------------------------------
# EJECUCIÓN
# -----------------------------------
if __name__ == "__main__":
    crear_grafica_doble_escala_corregida()
