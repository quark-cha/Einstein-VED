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
    - Cuadros "Fondation Einstein" y "Équations Fondamentales" en mismo nivel
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
    plt.suptitle('INTRICATION QUANTIQUE : Explication Géométrique Einstein-VED', 
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
    ax1.set_title('Cadre Interne : Temps Propre Partagé', fontweight='bold', fontsize=12)
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
    ax2.set_title('Cadre Externe : Perspective Conventionnelle', fontweight='bold', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # --- CUADRO DESCRIPTIVO IZQUIERDO ---
    texto_izquierdo = textwrap.fill(
        "SYMBOLOGIE :\n\n"
        "🔴 Particule A (45°)\n"
        "🟢 Particule B (225°)\n"
        "⚫ Observateur\n"
        "▬▬ Connexion géométrique\n"
        "▬▬ Lignes de visée",
        width=20
    )
    
    fig.text(0.02, 0.75, texto_izquierdo, 
             ha='left', va='center', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.6", facecolor="white", alpha=0.9,
                      edgecolor='gray', linewidth=1),
             transform=fig.transFigure)
    
    # --- CUADRO CENTRAL "FRONT D'ONDE" ---
    texto_central = textwrap.fill(
        "CLÉ EINSTEIN-VED :\n\n"
        "Les deux particules (y compris antipodales)\npartagent le même espace-temps propre t₀, s₀\n\n"
        "Car : dt' → 0 et ds' → 0 à la vitesse c\n\n"
        "t = t₀ + dt' → t₀\n"
        "s = s₀ + ds' → s₀\n\n"
        "Pas d'action à distance",
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
        "FONDATION EINSTEIN-VED :\n\n"
        "Les particules intriquées partagent un espace-temps propre commun depuis leur origine. "
        "Lorsqu'elles voyagent à la vitesse c, leurs différentielles de temps et d'espace propres tendent vers zéro "
        "(dt' → 0, ds' → 0), les maintenant connectées au même instant t₀ et position s₀. "
        "Cette simultanéité géométrique explique les corrélations quantiques sans violer la relativité.",
        width=45  # Más estrecho para caber al lado
    )
    
    fig.text(0.25, 0.35, texto_einstein,
             ha='center', va='center', fontsize=10.5, style='italic',
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#ffebee", alpha=0.9,
                      edgecolor='red', linewidth=2),
             transform=fig.transFigure)
    
    # CUADRO ECUACIONES (DERECHA) - MISMO NIVEL
    texto_ecuaciones = textwrap.fill(
        "ÉQUATIONS FONDAMENTALES :\n\n"
        "Pour les particules à la vitesse c :\n"
        "• dt' → 0, ds' → 0\n"
        "• t = t₀ + dt' → t₀\n" 
        "• s = s₀ + ds' → s₀\n\n"
        "Équation de champ :\n"
        "Gₘₙ + Λgₘₙ = (8πG/c⁴)Tₘₙ\n\n"
        "Simultanéité absolue dans le cadre propre",
        width=30
    )
    
    fig.text(0.75, 0.35, texto_ecuaciones, 
             ha='center', va='center', fontsize=10.5, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#f0f8ff", alpha=0.9,
                      edgecolor='blue', linewidth=2),
             transform=fig.transFigure)
    
    # --- TEXTO EXPLICATIVO INFERIOR ---
    texto_inferior = textwrap.fill(
        "INTERPRÉTATION EINSTEIN-VED : L'intrication quantique cesse d'être paradoxale lorsqu'elle est comprise "
        "depuis la géométrie de l'espace-temps. Les particules générées dans le même événement partagent un front d'onde "
        "où leur temps propre reste gelé à t₀. Cette simultanéité intrinsèque explique "
        "des corrélations parfaites sans 'action fantôme'. La probabilité quantique reflète "
        "la perspective limitée de l'observateur, pas une propriété fondamentale.",
        width=100
    )
    
    fig.text(0.5, 0.15, texto_inferior,
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#f5f5f5", alpha=0.8,
                      edgecolor='black', linewidth=1),
             transform=fig.transFigure)
    
    # Ajuste final del layout
    plt.tight_layout(rect=[0, 0.18, 1, 0.95])
    
    plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\FR_entrelazamiento_geometrico_final.svg", format='svg', 
                bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()
    print("✅ Guardado: entrelazamiento_geometrico_final.svg")

if __name__ == "__main__":
    print("🎯 CRÉATION DE LA VERSION FINALE AVEC CADRES AU MÊME NIVEAU...")
    crear_entrelazamiento_final()
    
    print("\n✨ CORRECTIONS APPLIQUÉES :")
    print("   • Cuadros 'Fondation Einstein' y 'Ecuaciones' en MISMO NIVEL")
    print("   • Figure plus large (16x10) pour accueillir les deux")
    print("   • Conception équilibrée et symétrique")
    print("   • Décoration et couleurs CONSERVÉES")
    print("   • ZÉRO chevauchements")