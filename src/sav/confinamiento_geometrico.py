# ANIMACIÓN SVG CONFINAMIENTO EINSTEIN-VED
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

def crear_animacion_confinamiento():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Parámetros comunes
    radius = 1.6
    wave_amplitude_factor = 0.3
    center_x, center_y = 5, 0
    n_cycles = 3  # ciclos completos en fase confinada

    # Configuración inicial
    ax.set_xlim(-1, 13)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    
    # Elementos de la animación
    line, = ax.plot([], [], 'b-', linewidth=3, label='Onda ψ(x)')
    
    # Ejes y etiquetas iniciales
    ax.set_xlabel('Posición x', fontsize=12)
    ax.set_ylabel('Amplitud ψ(x)', fontsize=12)
    ax.set_title('CONFINAMIENTO EINSTEIN-VED: Onda → Partícula', fontweight='bold', fontsize=14)
    
    def animate(frame):
        ax.clear()
        ax.set_xlim(-1, 13)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        if frame < 30:  # FASE 1: Onda completa en papel
            paper = patches.Rectangle((0, -1.5), 10, 3, fill=False, edgecolor='brown', linewidth=3)
            ax.add_patch(paper)
            x_show = np.linspace(0, 10, 500)
            y_show = np.sin(x_show)
            ax.plot(x_show, y_show, 'b-', linewidth=3)
            ax.set_xlabel('Posición x', fontsize=12)
            ax.set_ylabel('Amplitud ψ(x)', fontsize=12)
            ax.set_title('1. Onda Sinusoidal en Superficie Plana', fontweight='bold')
            for i in range(0, 11, 2):
                ax.axvline(i, color='gray', alpha=0.3, linestyle='--')
                ax.text(i, -1.8, str(i), ha='center')
        
        elif frame < 60:  # FASE 2: Transición
            progress = (frame - 30) / 30
            theta = np.linspace(0, np.pi, 100)
            x_points, y_points = [], []
            for angle in theta:
                x_flat = angle * (10/np.pi)
                x_circ = center_x + radius * np.cos(angle)
                y_circ = center_y + radius * np.sin(angle)
                x_points.append((1-progress)*x_flat + progress*x_circ)
                y_points.append((1-progress)*np.sin(x_flat) + progress*y_circ)
            ax.plot(x_points, y_points, 'b-', linewidth=3)
            if progress > 0.5:
                ax.plot([x_points[0], x_points[-1]], [y_points[0], y_points[-1]], 
                       'red', linewidth=2, linestyle='--', alpha=progress)
            ax.set_title(f'2. Transición: Enrollamiento ({progress*100:.0f}%)', fontweight='bold')
            ax.set_xlabel('Coordenada X')
            ax.set_ylabel('Coordenada Y')
        
        else:  # FASE 3: Confinamiento completo
            theta = np.linspace(0, n_cycles*2*np.pi, 1000)
            wave = wave_amplitude_factor * np.sin(n_cycles*theta)
            x_wave = center_x + (radius + wave) * np.cos(theta)
            y_wave = center_y + (radius + wave) * np.sin(theta)
            circle_x = center_x + radius * np.cos(theta)
            circle_y = center_y + radius * np.sin(theta)
            ax.plot(circle_x, circle_y, 'gray', linestyle='--', alpha=0.5, linewidth=1)
            ax.plot(x_wave, y_wave, 'red', linewidth=3, label=f'Confinada (n={n_cycles})')
            ax.text(0.4, -1.8, f'CONDICIÓN EINSTEIN-VED: L = {n_cycles}λ', 
                    fontweight='bold', fontsize=12,
                    bbox=dict(boxstyle="round", facecolor="yellow"))
            ax.set_title('3. Onda Auto-Confinada - Partícula Estable', fontweight='bold')
            ax.set_xlabel('Coordenada X')
            ax.set_ylabel('Coordenada Y')
            ax.legend()
        
        return line,
    
    anim = FuncAnimation(fig, animate, frames=90, interval=200, blit=False, repeat=True)
    
    # Guardar SVG de frames clave
    for frame in [0, 30, 60, 89]:
        animate(frame)
        plt.savefig(f'confinamiento_frame_{frame}.svg', format='svg', bbox_inches='tight')
        print(f"SVG guardado: confinamiento_frame_{frame}.svg")
    
    plt.tight_layout()
    plt.show()
    
    return anim

# Resumen estático coherente
def generar_resumen_confinamiento():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    radius = 1.6
    wave_amplitude_factor = 0.3
    center_x, center_y = 5, 0
    n_cycles = 3

    # Estado 1: Onda plana
    ax1 = axes[0]
    paper = patches.Rectangle((0, -1.2), 8, 2.4, fill=False, edgecolor='brown', linewidth=2)
    ax1.add_patch(paper)
    x = np.linspace(0, 8, 300)
    y = np.sin(x)
    ax1.plot(x, y, 'b-', linewidth=3)
    ax1.set_xlim(-1, 9)
    ax1.set_ylim(-2, 2)
    ax1.set_aspect('equal')
    ax1.set_title('a) Onda Plana Libre', fontweight='bold')
    ax1.set_xlabel('Posición x')
    ax1.set_ylabel('Amplitud ψ(x)')
    ax1.grid(True, alpha=0.3)

    # Estado 2: Transición
    ax2 = axes[1]
    theta = np.linspace(0, np.pi, 200)
    x_trans, y_trans = [], []
    for angle in theta:
        x_flat = angle * (8/np.pi)
        x_circ = center_x + radius * np.cos(angle)
        y_circ = center_y + radius * np.sin(angle)
        x_trans.append(0.5*x_flat + 0.5*x_circ)
        y_trans.append(0.5*np.sin(x_flat) + 0.5*y_circ)
    ax2.plot(x_trans, y_trans, 'orange', linewidth=3)
    ax2.set_xlim(0, 8)
    ax2.set_ylim(-2, 2)
    ax2.set_aspect('equal')
    ax2.set_title('b) Transición', fontweight='bold')
    ax2.set_xlabel('Coordenada X')
    ax2.set_ylabel('Coordenada Y')
    ax2.grid(True, alpha=0.3)

    # Estado 3: Confinado n=3
    ax3 = axes[2]
    theta = np.linspace(0, n_cycles*2*np.pi, 1000)
    wave = wave_amplitude_factor * np.sin(n_cycles*theta)
    x_wave = center_x + (radius + wave) * np.cos(theta)
    y_wave = center_y + (radius + wave) * np.sin(theta)
    circle_x = center_x + radius * np.cos(theta)
    circle_y = center_y + radius * np.sin(theta)
    ax3.plot(circle_x, circle_y, 'gray', linestyle='--', alpha=0.5)
    ax3.plot(x_wave, y_wave, 'red', linewidth=3)
    ax3.set_xlim(0, 8)
    ax3.set_ylim(-2, 2)
    ax3.set_aspect('equal')
    ax3.set_title('c) Confinado n=3\nL = 3λ', fontweight='bold')
    ax3.set_xlabel('Coordenada X')
    ax3.set_ylabel('Coordenada Y')
    ax3.grid(True, alpha=0.3)
    ax3.text(1.6, -1.3, 'CONDICIÓN: L = nλ', ha='center', fontweight='bold',
             bbox=dict(boxstyle="round", facecolor="yellow"))

    plt.tight_layout()
    plt.savefig('confinamiento.svg', format='svg', bbox_inches='tight')
    plt.show()
    print("SVG resumen guardado: 'resumen_confinamiento.svg'")

# Ejecutar
print("Generando animación SVG del confinamiento...")
crear_animacion_confinamiento()
generar_resumen_confinamiento()
print("✅ Animación SVG completada")

if __name__ == "__main__":
    print("Generando animación SVG del confinamiento...")
    crear_animacion_confinamiento()
    generar_resumen_confinamiento()
    print("✅ Animación SVG completada")