import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D

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

def crear_tabla_valores():
    import textwrap
    fig, ax = plt.subplots(figsize=(10,5))
    ax.axis('off')

    mc_min, mc_mean, mc_max = calcular_rango_3sigma(MC_mean, MC_sigma)
    lhc_min, lhc_mean, lhc_max = calcular_rango_3sigma(LHC_mean, LHC_sigma)
    ved_min, ved_mean, ved_max = calcular_rango_3sigma(VED_mean, VED_sigma)

    # Función para envolver texto
    def wrap_text(text, width=15):
        return '\n'.join(textwrap.wrap(str(text), width=width))

    table_data = [
        ['Theory','Mean Radius (fm)','Min (fm)','Max (fm)','Uncertainty','Precision'],
        [wrap_text('Quantum Mechanics (MC)'), f"{mc_mean:.3f}", f"{mc_min:.3f}", f"{mc_max:.3f}", f"±{MC_sigma:.3f}", wrap_text("Low")],
        [wrap_text('LHC Experimental'), f"{lhc_mean:.5f}", f"{lhc_min:.5f}", f"{lhc_max:.5f}", f"±{LHC_sigma:.3f}", wrap_text("Reference")],
        [wrap_text('Einstein-VED'), f"{ved_mean:.5f}", f"{ved_min:.5f}", f"{ved_max:.5f}", f"±{VED_sigma:.5f}", wrap_text("High (99.96%)")]
    ]

    tbl = ax.table(cellText=table_data, loc='center', cellLoc='center', colLoc='center', rowLoc='center')

    # Desactivar auto ajuste de tamaño
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)

    # Escalar celdas a lo ancho y alto
    tbl.scale(1.4, 2.2)  # ancho x altura

    # Colores por fila (opcional, mejora visual)
    row_colors = [None, c_MC, c_LHC, c_VED]
    for i, color in enumerate(row_colors):
        if color:
            for j in range(len(table_data[0])):
                tbl[(i, j)].set_facecolor(color)
                tbl[(i, j)].set_alpha(0.3)

    plt.tight_layout()
    plt.savefig('proton_table_full.svg', format='svg', dpi=300)
    plt.show()
    plt.close()
    print("✅ Guardado: proton_table_full.svg")

class EinsteinVEDVisualizer:
    def __init__(self):
        self.fig_size = (12, 8)
        plt.style.use('default')
        
    def create_confinement_geometry(self):
        """Figura 1: Geometrías de confinamiento 2D vs 3D"""
        fig = plt.figure(figsize=(14, 10))
        gs = gridspec.GridSpec(2, 3, figure=fig)
        
        # Electrón - Confinamiento 2D (superficie)
        ax1 = fig.add_subplot(gs[0, 0], projection='3d')
        self._plot_electron_surface(ax1)
        ax1.set_title('Electrón: Confinamiento 2D\nn = 137 (Superficie)', fontsize=12, fontweight='bold')
        
        # Protón - Confinamiento 3D
        ax2 = fig.add_subplot(gs[0, 1], projection='3d')
        self._plot_proton_volume(ax2)
        ax2.set_title('Protón: Confinamiento 3D\nn = 4 (Volumen)', fontsize=12, fontweight='bold')
        
        # Quarks - Dipolos dimensionales
        ax3 = fig.add_subplot(gs[0, 2])
        self._plot_quark_dipoles(ax3)
        ax3.set_title('Quarks: Dipolos Geométricos\nAnclaje 3D', fontsize=12, fontweight='bold')
        
        # Comparación dimensional
        ax4 = fig.add_subplot(gs[1, :])
        self._plot_dimensional_comparison(ax4)
        ax4.set_title('Estadística Cuántica Emergente: 2D vs 3D', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def _plot_electron_surface(self, ax):
        """Superficie 2D del electrón - ESCALAS LIMPIAS"""
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        r = 1.0
        
        x = r * np.outer(np.cos(u), np.sin(v))
        y = r * np.outer(np.sin(u), np.sin(v))
        z = r * np.outer(np.ones(np.size(u)), np.cos(v))
        
        color = plt.cm.viridis(0.6)
        
        surf = ax.plot_surface(x, y, z, color=color, alpha=0.8, 
                              rstride=2, cstride=2, linewidth=0)
        
        # LIMPIAR ESCALAS - solo mostrar -1, 0, 1
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
        
        # Configurar ticks simples
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.set_zticks([-1, 0, 1])
        
        # Etiquetas más limpias
        ax.set_xlabel('X', labelpad=10)
        ax.set_ylabel('Y', labelpad=10)
        ax.set_zlabel('Z', labelpad=10)
        
        ax.view_init(elev=30, azim=45)
        
    def _plot_proton_volume(self, ax):
        """Volumen 3D del protón - ESCALAS LIMPIAS"""
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 30)
        r = 1.0
        
        x = r * np.outer(np.cos(u), np.sin(v))
        y = r * np.outer(np.sin(u), np.sin(v))
        z = r * np.outer(np.ones(np.size(u)), np.cos(v))
        
        color = plt.cm.plasma(0.7)
        
        surf = ax.plot_surface(x, y, z, color=color, alpha=0.9, 
                              rstride=1, cstride=1, linewidth=0)
        
        # LIMPIAR ESCALAS
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_zlim(-1.2, 1.2)
        
        # Ticks simples
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.set_zticks([-1, 0, 1])
        
        # Ejes dimensionales más limpios
        scale = 1.2
        ax.quiver(0, 0, 0, scale, 0, 0, color='red', linewidth=2, label='X')
        ax.quiver(0, 0, 0, 0, scale, 0, color='green', linewidth=2, label='Y')
        ax.quiver(0, 0, 0, 0, 0, scale, color='blue', linewidth=2, label='Z')
        
        ax.set_xlabel('X', labelpad=10)
        ax.set_ylabel('Y', labelpad=10)
        ax.set_zlabel('Z', labelpad=10)
        
        ax.view_init(elev=20, azim=30)
        # Leyenda más compacta
        ax.legend(loc='upper left', bbox_to_anchor=(0, 1))
        
    def _plot_quark_dipoles(self, ax):
        """Dipolos de quarks anclados a dimensiones"""
        positions = [(0, 0.5), (-0.4, -0.3), (0.4, -0.3)]
        colors = ['red', 'green', 'blue']
        dimensions = ['X', 'Y', 'Z']
        
        for (x, y), color, dim in zip(positions, colors, dimensions):
            if dim == 'X':
                ax.arrow(x-0.3, y, 0.6, 0, head_width=0.1, head_length=0.1, 
                        fc=color, ec=color, linewidth=3)
            elif dim == 'Y':
                ax.arrow(x, y-0.3, 0, 0.6, head_width=0.1, head_length=0.1,
                        fc=color, ec=color, linewidth=3)
            else:
                circle = Circle((x, y), 0.2, fill=True, color=color, alpha=0.7)
                ax.add_patch(circle)
            
            ax.text(x, y+0.4, f'Quark {dim}', ha='center', fontweight='bold', fontsize=10)
        
        confinement_circle = Circle((0, 0), 0.8, fill=False, linestyle='--', 
                                  color='black', linewidth=2)
        ax.add_patch(confinement_circle)
        ax.text(0, -1.1, 'Confinamiento Hadrónico', ha='center', fontsize=12, fontweight='bold')
        
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
        
    def _plot_dimensional_comparison(self, ax):
        """Comparación estadística Fermi vs Bose"""
        categories = ['Confinamiento 2D\n(Electrón)', 'Confinamiento 3D\n(Protón)']
        fermi_stats = [1, 0]
        bose_stats = [0, 1]
        
        x = np.arange(len(categories))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, fermi_stats, width, label='Fermi-Dirac (Exclusión)', 
                      color='red', alpha=0.7)
        bars2 = ax.bar(x + width/2, bose_stats, width, label='Bose-Einstein (Condensación)', 
                      color='blue', alpha=0.7)
        
        ax.set_ylabel('Comportamiento Estadístico', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, fontweight='bold')
        ax.legend()
        
        ax.text(0, 0.8, 'Máximo 1 partícula\npor estado', ha='center', fontweight='bold')
        ax.text(1, 0.8, 'Múltiples partículas\nmismo estado', ha='center', fontweight='bold')
        
        ax.set_ylim(0, 1.2)
        
    def create_experimental_validation(self):
        """Figura 2: Validación experimental"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # Gráfico 1: Radios
        particles = ['Protón VED', 'Protón LHC', 'Neutrón VED', 'Neutrón Exp']
        radii = [0.84118, 0.84087, 0.84367, 0.84200]
        errors = [0, 0.014, 0, 0.015]
        colors = ['red', 'lightcoral', 'blue', 'lightblue']
        
        bars = ax1.bar(particles, radii, yerr=errors, capsize=5, color=colors, alpha=0.8)
        ax1.set_ylabel('Radio (fm)', fontweight='bold')
        ax1.set_title('Predicción de Radios Hadrónicos', fontweight='bold', fontsize=12)
        
        for bar, radius in zip(bars, radii):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.002,
                    f'{radius:.5f}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 2: Precisión
        theories = ['Einstein-VED', 'QCD Retículo', 'Modelo Constituyente']
        precision = [99.96, 95.0, 85.0]
        
        bars2 = ax2.bar(theories, precision, color=['green', 'orange', 'red'], alpha=0.7)
        ax2.set_ylabel('Precisión (%)', fontweight='bold')
        ax2.set_title('Comparación de Precisiones', fontweight='bold', fontsize=12)
        
        for bar, prec in zip(bars2, precision):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{prec}%', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 3: Constante estructura fina
        alpha_inv = 137.035999084
        ved_prediction = 137.0
        
        theories = ['Experimental', 'Einstein-VED']
        values = [alpha_inv, ved_prediction]
        colors = ['red', 'blue']
        
        bars3 = ax3.bar(theories, values, color=colors, alpha=0.7)
        ax3.set_ylabel('α⁻¹', fontweight='bold')
        ax3.set_title('Constante de Estructura Fina', fontweight='bold', fontsize=12)
        
        for bar, value in zip(bars3, values):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 4: Explicación
        ax4.axis('off')
        explanation_text = (
            "EXPLICACIÓN DIPOLAR DE JETS EN LHC:\n\n"
            "• Quarks = Dipolos geométricos anclados a dimensiones\n"
            "• Al aplicar energía: ruptura dipolar\n"
            "• Creación de nuevos pares quark-antiquark\n"
            "• Formación de jets hadrónicos en direcciones opuestas\n"
            "• No hay 'fuerza de confinamiento' infinita\n"
            "• Solo reconfiguración geométrica natural"
        )
        ax4.text(0.1, 0.9, explanation_text, transform=ax4.transAxes, fontsize=11,
                verticalalignment='top', bbox=dict(boxstyle="round", facecolor='lightgray'))
        
        plt.tight_layout()
        return fig

    def create_quantum_paradox_solution(self):
        """Figura 3: Solución a paradojas cuánticas"""
        fig = plt.figure(figsize=(16, 12))
        gs = gridspec.GridSpec(2, 2, figure=fig)
        
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_double_slit_solution(ax1)
        
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_entanglement_solution(ax2)
        
        ax3 = fig.add_subplot(gs[1, 0])
        self._plot_wavefunction_solution(ax3)
        
        ax4 = fig.add_subplot(gs[1, 1])
        self._plot_quantum_statistics_solution(ax4)
        
        plt.tight_layout()
        return fig

    def _plot_double_slit_solution(self, ax):
        """Solución a la doble rendija"""
        slits = [-0.5, 0.5]
        screen_x = 3
        
        for slit in slits:
            ax.plot([0, 0], [slit-0.1, slit+0.1], 'k-', linewidth=3)
        
        x_pattern = np.linspace(0.5, 2.5, 100)
        y_pattern = np.linspace(-1, 1, 100)
        
        for x in x_pattern[::10]:
            for y in y_pattern[::10]:
                intensity = np.exp(-x/2) * (np.cos(10*y) + 1)/2
                if intensity > 0.3:
                    ax.plot(x, y, 'bo', alpha=intensity, markersize=2)
        
        ax.set_xlim(-1, 3)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlabel('Dirección de propagación')
        ax.set_ylabel('Posición')
        ax.set_title('SOLUCIÓN DOBLE RENDIJA:\nSuperficie completa interactúa', 
                    fontweight='bold', fontsize=11)
        
        ax.text(1.5, -1.2, 'No es "partícula por dos caminos"\nEs SUPERFICIE por ambos', 
               ha='center', fontweight='bold', bbox=dict(facecolor='white', alpha=0.8))

    def _plot_entanglement_solution(self, ax):
        """Solución geométrica al entrelazamiento"""
        wave_front = Ellipse((0, 0), 4, 2, fill=False, linestyle='-', 
                           color='blue', linewidth=2, alpha=0.7)
        ax.add_patch(wave_front)
        
        particle1 = Circle((-1.5, 0), 0.2, fill=True, color='red')
        particle2 = Circle((1.5, 0), 0.2, fill=True, color='green')
        ax.add_patch(particle1)
        ax.add_patch(particle2)
        
        ax.plot([-1.3, 1.3], [0, 0], 'k--', alpha=0.5, linewidth=1)
        
        ax.text(-1.5, 0.5, 'Partícula A', ha='center', fontweight='bold')
        ax.text(1.5, 0.5, 'Partícula B', ha='center', fontweight='bold')
        ax.text(0, -1.2, 'GEOMETRÍA COMPARTIDA', ha='center', fontweight='bold', 
               bbox=dict(facecolor='yellow', alpha=0.7))
        
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.set_title('ENTRELAZAMIENTO:\nGeometría común, no acción a distancia', 
                    fontweight='bold', fontsize=11)
        ax.axis('off')

    def _plot_wavefunction_solution(self, ax):
        """Solución al colapso de la función de onda"""
        x = np.linspace(-2, 2, 200)
        
        actual_geometry = np.exp(-x**2 / 0.5)
        mc_probability = np.exp(-x**2 / 0.3)
        
        ax.plot(x, actual_geometry, 'g-', linewidth=3, label='Geometría real (siempre definida)')
        ax.plot(x, mc_probability, 'r--', linewidth=2, label='MC: "Probabilidad antes de medir"')
        
        measure_point = 0.5
        ax.axvline(x=measure_point, color='black', linestyle=':', alpha=0.7)
        ax.plot(measure_point, np.exp(-measure_point**2 / 0.5), 'ko', markersize=8)
        
        ax.set_xlabel('Posición')
        ax.set_ylabel('Amplitud')
        ax.set_title('FIN DEL "COLAPSO":\nGeometría definida, no probabilística', 
                    fontweight='bold', fontsize=11)
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_quantum_statistics_solution(self, ax):
        """Solución a la estadística cuántica"""
        ax.axis('off')
        
        explanation_text = (
            "ESTADÍSTICA CUÁNTICA EMERGENTE\n\n"
            "Fermi-Dirac (Exclusión):\n"
            "• Confinamiento 2D (electrón)\n"
            "• Restricción topológica natural\n"
            "• Solo 1 partícula por estado\n\n"
            "Bose-Einstein (Condensación):\n"  
            "• Confinamiento 3D (protón)\n"
            "• Geometría esférica completa\n"
            "• Múltiples partículas mismo estado\n\n"
            "NO son propiedades fundamentales\n"
            "SON consecuencias geométricas"
        )
        
        ax.text(0.1, 0.9, explanation_text, transform=ax.transAxes, fontsize=11,
                verticalalignment='top', fontweight='bold',
                bbox=dict(boxstyle="round", facecolor='lightblue', alpha=0.8))

    def save_all_figures(self, format='png', dpi=300):
        """Guarda todas las figuras"""
        figures = []
        
        print("Generando visualizaciones Einstein-VED...")
        
        try:
            print("Generando Figura 1: Geometrías de confinamiento...")
            fig1 = self.create_confinement_geometry()
            fig1.savefig('VED_Geometrias_Confinamiento.png', format=format, dpi=dpi, 
                        bbox_inches='tight')
            figures.append(fig1)
            plt.show()
            plt.close(fig1)
            print("✓ Geometrías de confinamiento guardadas")
            
            print("Generando Figura 2: Validación experimental...")
            fig2 = self.create_experimental_validation()
            fig2.savefig('VED_Validacion_Experimental.png', format=format, dpi=dpi,
                        bbox_inches='tight')
            figures.append(fig2)
            plt.show()
            plt.close(fig2)
            print("✓ Validación experimental guardada")
            
            print("Generando Figura 3: Solución paradojas cuánticas...")
            fig3 = self.create_quantum_paradox_solution()
            fig3.savefig('VED_Solucion_Paradojas.png', format=format, dpi=dpi,
                        bbox_inches='tight')
            figures.append(fig3)
            plt.close(fig3)
            print("✓ Solución paradojas cuánticas guardada")
            
            print(f"\n✅ Todas las figuras guardadas en formato {format} (DPI: {dpi})")
            
        except Exception as e:
            print(f"❌ Error durante la generación: {e}")
            
        return figures

# Ejemplo de uso
if __name__ == "__main__":
    visualizer = EinsteinVEDVisualizer()
    
    print("Iniciando generación de visualizaciones Einstein-VED...")
    crear_tabla_valores()
    
    figures = visualizer.save_all_figures()
    
    print("\n🎨 Visualizaciones completadas!")
    print("Archivos generados:")
    print("• VED_Geometrias_Confinamiento.png")
    print("• VED_Validacion_Experimental.png") 
    print("• VED_Solucion_Paradojas.png")