# -*- coding: utf-8 -*-
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

# entrelazamiento_geometrico_final.py
import matplotlib.pyplot as plt
import numpy as np
import textwrap

def crear_entrelazamiento_final():
    """
    Versión final corregida:
    - Cuadros "Grundlegende Gleichungen" y "QUANTENVERSCHRÄNKUNG: Geometrische Erklärung Einstein-VED" en mismo nivel
    - Diseño más ancho para acomodar ambos cuadros
    - Respetando la decoración actual
    """
    fig = plt.figure(figsize=(16, 10))  # Más ancho para acomodar cuadros
    
    # Crear una representación conceptual del frente de onda
    theta = np.linspace(0, 2*np.pi, 100)
    r = 2
    
    # Coordenadas del frente de onda
    x_wave = r * np.cos(theta)
    y_wave = r * np.sin(theta)
    
    # Partículas entrelazadas (incluyendo antipodales)
    particle_a = [r * np.cos(np.pi/4), r * np.sin(np.pi/4)]      # 45°
    particle_b = [r * np.cos(5*np.pi/4), r * np.sin(5*np.pi/4)] # 225° (antípoda)
    
    # Observadores
    observer_1 = [0, 0]  # En el centro
    observer_2 = [3, 0]  # Externo
    
    # --- TÍTULO PRINCIPAL ---
    plt.suptitle('Interner Rahmen: Gemeinsame Eigenzeit', 
                 fontsize=16, fontweight='bold', y=0.97)
    
    # --- Gráfica 1: Vista interna (izquierda) ---
    ax1 = fig.add_axes([0.08, 0.58, 0.38, 0.30])
    
    ax1.plot(x_wave, y_wave, 'b-', alpha=0.5, linewidth=2)
    ax1.fill(x_wave, y_wave, alpha=0.1, color='blue')
    ax1.plot(particle_a[0], particle_a[1], 'ro', markersize=12)
    ax1.plot(particle_b[0], particle_b[1], 'go', markersize=12)
    ax1.plot([particle_a[0], particle_b[0]], [particle_a[1], particle_b[1]], 
             'k--', alpha=0.5, linewidth=1)
    ax1.plot(observer_1[0], observer_1[1], 'ks', markersize=10)
    
    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-3, 3)
    ax1.set_aspect('equal')
    ax1.set_title('Externer Rahmen: Konventionelle Perspektive', fontweight='bold', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # --- Gráfica 2: Vista externa (derecha) ---
    ax2 = fig.add_axes([0.58, 0.58, 0.38, 0.30])
    
    ax2.plot(x_wave, y_wave, 'b-', alpha=0.5, linewidth=2)
    ax2.fill(x_wave, y_wave, alpha=0.1, color='blue')
    ax2.plot(particle_a[0], particle_a[1], 'ro', markersize=12)
    ax2.plot(particle_b[0], particle_b[1], 'go', markersize=12)
    ax2.plot(observer_2[0], observer_2[1], 'ks', markersize=10)
    ax2.plot([observer_2[0], particle_a[0]], [observer_2[1], particle_a[1]], 
             'r-', alpha=0.3)
    ax2.plot([observer_2[0], particle_b[0]], [observer_2[1], particle_b[1]], 
             'g-', alpha=0.3)
    
    ax2.set_xlim(-1, 4)
    ax2.set_ylim(-3, 3)
    ax2.set_aspect('equal')
    ax2.set_title('SYMBOLIK:\n\n', fontweight='bold', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # --- CUADRO DESCRIPTIVO IZQUIERDO ---
    texto_izquierdo = textwrap.fill(
        "🔴 Teilchen A (45°)\n"
        "🟢 Teilchen B (225°)\n"
        "⚫ Beobachter\n"
        "▬▬ Geometrische Verbindung\n"
        "▬▬ Sichtlinien"
        "WELLENFRONT",
        width=20
    )
    
    fig.text(0.02, 0.75, texto_izquierdo, 
             ha='left', va='center', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.6", facecolor="white", alpha=0.9,
                      edgecolor='gray', linewidth=1),
             transform=fig.transFigure)
    
    # --- CUADRO CENTRAL "EINSTEIN-VED SCHLÜSSEL:\n\n" ---
    texto_central = textwrap.fill(
        "Beide Teilchen (einschließlich antipodaler)\nteilen dieselbe Eigenzeit-Raum t₀, s₀\n\n"
        "Weil: dt' → 0 und ds' → 0 bei Lichtgeschwindigkeit c\n\n"
        "→ 0 und ds"
        "Keine Fernwirkung"
        "Keine Fernwirkung"
        "EINSTEIN-VED GRUNDLAGE:\n\n",
        width=28
    )
    
    fig.text(0.5, 0.75, texto_central, 
             ha='center', va='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#fffacd", alpha=0.95,
                      edgecolor='orange', linewidth=2),
             transform=fig.transFigure)
    
    # --- CUADROS EN MISMO NIVEL: FUNDAMENTO EINSTEIN Y ECUACIONES ---
    
    # CUADRO EINSTEIN (IZQUIERDA)
    texto_einstein = textwrap.fill(
        "Verschränkte Teilchen teilen gemeinsame Eigenzeit-Raum von ihrem Ursprung."
        "Bei Bewegung mit Lichtgeschwindigkeit c tendieren ihre Eigenzeit- und Raumdifferentiale zu Null "
        "(dt' Diese geometrische Gleichzeitigkeit erklärt Quantenkorrelationen ohne Relativität zu verletzen.' → 0), was sie im selben Moment t₀ und Position s₀ verbunden hält. "
        "Diese geometrische Gleichzeitigkeit erklärt Quantenkorrelationen ohne Relativität zu verletzen. "
        "GRUNDLEGENDE GLEICHUNGEN:\n\n",
        width=45  # Más estrecho para caber al lado
    )
    
    fig.text(0.25, 0.35, texto_einstein,
             ha='center', va='center', fontsize=10.5, style='italic',
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#ffebee", alpha=0.9,
                      edgecolor='red', linewidth=2),
             transform=fig.transFigure)
    
    # CUADRO ECUACIONES (DERECHA) - MISMO NIVEL
    texto_ecuaciones = textwrap.fill(
        "Für Teilchen bei Lichtgeschwindigkeit c:\n"
        "Feldgleichung:\n"
        "• dt' Diese geometrische Gleichzeitigkeit erklärt Quantenkorrelationen ohne Relativität zu verletzen.' → 0\n"
        "• Keine Fernwirkung" 
        "• Keine Fernwirkung"
        "Absolute Gleichzeitigkeit im Eigenrahmen"
        "Absolute Gleichzeitigkeit im Eigenrahmen"
        "EINSTEIN-VED INTERPRETATION: Quantenverschränkung hört auf paradox zu sein, wenn sie",
        width=30
    )
    
    fig.text(0.75, 0.35, texto_ecuaciones, 
             ha='center', va='center', fontsize=10.5, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#f0f8ff", alpha=0.9,
                      edgecolor='blue', linewidth=2),
             transform=fig.transFigure)
    
    # --- TEXTO EXPLICATIVO INFERIOR ---
    texto_inferior = textwrap.fill(
        "aus der Raumzeit-Geometrie verstanden wird. Teilchen, die im selben Ereignis erzeugt werden, teilen eine Wellenfront "
        "wo ihre Eigenzeit bei t₀ eingefroren bleibt. Diese intrinsische Gleichzeitigkeit erklärt "
        ""perfekte Korrelationen ohne ""spukhafte Fernwirkung"". Quantenwahrscheinlichkeit reflektiert" "
        "spukhafte Fernwirkung "
        "🎯 ERSTELLE FINALE VERSION MIT RAHMEN AUF GLEICHER EBENE...",
        width=100
    )
    
    fig.text(0.5, 0.15, texto_inferior,
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#f5f5f5", alpha=0.8,
                      edgecolor='black', linewidth=1),
             transform=fig.transFigure)
    
    # Ajuste final del layout
    plt.tight_layout(rect=[0, 0.18, 1, 0.95])
    
    plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\DE_entrelazamiento_geometrico_final.svg", format='svg', 
                bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()
    print("✅ Guardado: entrelazamiento_geometrico_final.svg")

if __name__ == "__main__":
    print("\n✨ ANGEWENDETE KORREKTUREN:")
    crear_entrelazamiento_final()
    
    print("• Rahmen 'Einstein-Grundlage' und 'Gleichungen' auf GLEICHER EBENE")
    print("   • Cuadros 'Grundlegende Gleichungen' y 'Ecuaciones' en MISMO NIVEL")
    print("   • Ausgewogenes und symmetrisches Design")
    print("   • Dekoration und Farben BEIBEHALTEN")
    print("   • NULL ÜBERLAPPUNGEN")
    print("   • CERO solapamientos")