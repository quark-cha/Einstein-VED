# -*- coding: utf-8 -*-
# ANIMACIÓN SVG CONFINAMIENTO EINSTEIN-VED
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
    line, = ax.plot([], [], 'b-', linewidth=3, label='Welle ψ(x)')
    
    # Ejes y etiquetas iniciales
    ax.set_xlabel('Position x', fontsize=12)
    ax.set_ylabel('Amplitude ψ(x)', fontsize=12)
    ax.set_title('EINSTEIN-VED CONFINEMENT: Welle → Teilchen', fontweight='bold', fontsize=14)
    
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
            ax.set_xlabel('Position x', fontsize=12)
            ax.set_ylabel('Amplitude ψ(x)', fontsize=12)
            ax.set_title('1. Sinuswelle auf ebener Oberfläche', fontweight='bold')
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
            ax.set_title(f'2. Übergang: Aufrollen ({progress*100:.0f}%)', fontweight='bold')
            ax.set_xlabel('X-Koordinate')
            ax.set_ylabel('Y-Koordinate')
        
        else:  # FASE 3: Confinamiento completo
            theta = np.linspace(0, n_cycles*2*np.pi, 1000)
            wave = wave_amplitude_factor * np.sin(n_cycles*theta)
            x_wave = center_x + (radius + wave) * np.cos(theta)
            y_wave = center_y + (radius + wave) * np.sin(theta)
            circle_x = center_x + radius * np.cos(theta)
            circle_y = center_y + radius * np.sin(theta)
            ax.plot(circle_x, circle_y, 'gray', linestyle='--', alpha=0.5, linewidth=1)
            ax.plot(x_wave, y_wave, 'red', linewidth=3, label=f'Eingeschlossen (n={n_cycles})')
            ax.text(0.4, -1.8, f'EINSTEIN-VED BEDINGUNG: L = {n_cycles}λ', 
                    fontweight='bold', fontsize=12,
                    bbox=dict(boxstyle="round", facecolor="yellow"))
            ax.set_title('3. Selbst-eingeschlossene Welle - stabiles Teilchen', fontweight='bold')
            ax.set_xlabel('X-Koordinate')
            ax.set_ylabel('Y-Koordinate')
            ax.legend()
        
        return line,
    
    anim = FuncAnimation(fig, animate, frames=90, interval=200, blit=False, repeat=True)
    
    # Guardar SVG de frames clave
    for frame in [0, 30, 60, 89]:
        animate(frame)
        plt.savefig(f'confinamiento_frame_{frame}.svg', format='svg', bbox_inches='tight')
        print(f"SVG guardado: confinamiento_frame_{frame}.svg")
    
    plt.tight_layout()
    
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
    ax1.set_title('a) Freie ebene Welle', fontweight='bold')
    ax1.set_xlabel('Position x')
    ax1.set_ylabel('Amplitude ψ(x)')
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
    ax2.set_title('b) Übergang', fontweight='bold')
    ax2.set_xlabel('X-Koordinate')
    ax2.set_ylabel('Y-Koordinate')
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
    ax3.set_title('c) Eingeschlossen n=3\nL = 3λ', fontweight='bold')
    ax3.set_xlabel('X-Koordinate')
    ax3.set_ylabel('Y-Koordinate')
    ax3.grid(True, alpha=0.3)
    ax3.text(1.6, -1.3, 'BEDINGUNG: L = nλ', ha='center', fontweight='bold',
             bbox=dict(boxstyle="round", facecolor="yellow"))

    plt.tight_layout()
    plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\DE_confinamiento.svg", format='svg', bbox_inches='tight')
    print("SVG resumen guardado: 'resumen_confinamiento.svg'")

# Ejecutar
print("Erzeuge SVG-Animation des Confinements...")
crear_animacion_confinamiento()
generar_resumen_confinamiento()
print("✅ SVG-Animation abgeschlossen")

if __name__ == "__main__":
    print("Erzeuge SVG-Animation des Confinements...")
    crear_animacion_confinamiento()
    generar_resumen_confinamiento()
    print("✅ SVG-Animation abgeschlossen")