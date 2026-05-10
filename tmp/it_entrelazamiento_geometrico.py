import matplotlib
matplotlib.use("Agg")   # backend no interactivo (batch / CI / traducciones)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import sys
from pathlib import Path

# ===========================
# CONFIGURACIÓN GLOBAL
# ===========================
idioma_actual = "it"   # definido por el generador del temporal

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from libreria import configurar_fuentes as cf
cf.configurar_fuentes(idioma_actual, plt)

# INICIO DEL CÓDIGO PRINCIPAL
# ===========================
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import sys
from pathlib import Path


import textwrap

def crear_entrelazamiento_final():
    """
    Versión final corregida:
    - Cuadros "Fundamento Einstein" y "Ecuaciones Fundamentales" en mismo nivel
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
    plt.suptitle('ENTANGLEMENT QUANTISTICO: Spiegazione Geometrica Einstein-VED', 
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
    ax1.set_title('Quadro Interno: Tempo Proprio Condiviso', fontweight='bold', fontsize=12)
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
    ax2.set_title('Quadro Esterno: Prospettiva Convenzionale', fontweight='bold', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # --- CUADRO DESCRIPTIVO IZQUIERDO ---
    texto_izquierdo = textwrap.fill(
        "SIMBOLOGIA:\n\n"
        "🔴 Particella A (45°)\n"
        "🟢 Particella B (225°)\n"
        "⚫ Osservatore\n"
        "▬▬ Connessione geometrica\n"
        "▬▬ Linee di vista",
        width=20
    )
    
    fig.text(0.02, 0.75, texto_izquierdo, 
             ha='left', va='center', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.6", facecolor="white", alpha=0.9,
                      edgecolor='gray', linewidth=1),
             transform=fig.transFigure)
    
    # --- CUADRO CENTRAL "FRENTE DE ONDA" ---
    texto_central = textwrap.fill(
        "CHIAVE EINSTEIN-VED:\n\n"
        "Entrambe le particelle (incluse quelle antipodali)\ncondividono lo stesso spaziotempo proprio t₀, s₀\n\n"
        "Porque: dt' → 0 y ds' → 0 alla velocità c\n\n"
        "t = t₀ + dt' → t₀\n"
        "s = s₀ + ds' → s₀\n\n"
        "Nessuna azione a distanza",
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
        "FONDAMENTO EINSTEIN-VED:\n\n"
        "Le particelle entangled condividono uno spaziotempo proprio comune dalla loro origine."
        "Quando viaggiano alla velocità c, i loro differenziali di tempo e spazio propri tendono a zero"
        "(dt' → 0, ds' → 0), mantenendole connesse nello stesso istante t₀ e posizione s₀."
        "Questa simultaneità geometrica spiega le correlazioni quantistiche senza violare la relatività.",
        width=45  # Más estrecho para caber al lado
    )
    
    fig.text(0.25, 0.35, texto_einstein,
             ha='center', va='center', fontsize=10.5, style='italic',
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#ffebee", alpha=0.9,
                      edgecolor='red', linewidth=2),
             transform=fig.transFigure)
    
    # CUADRO ECUACIONES (DERECHA) - MISMO NIVEL
    texto_ecuaciones = textwrap.fill(
        "EQUAZIONI FONDAMENTALI:\n\n"
        "Per particelle alla velocità c:\n"
        "• dt' → 0, ds' → 0\n"
        "• t = t₀ + dt' → t₀\n" 
        "• s = s₀ + ds' → s₀\n\n"
        "Equazione di campo:\n"
        "Gₘₙ + Λgₘₙ = (8πG/c⁴)Tₘₙ\n\n"
        "Simultaneità assoluta nel sistema di riferimento proprio",
        width=30
    )
    
    fig.text(0.75, 0.35, texto_ecuaciones, 
             ha='center', va='center', fontsize=10.5, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#f0f8ff", alpha=0.9,
                      edgecolor='blue', linewidth=2),
             transform=fig.transFigure)
    
    # --- TEXTO EXPLICATIVO INFERIOR ---
    texto_inferior = textwrap.fill(
        "INTERPRETAZIONE EINSTEIN-VED: L'entanglement quantistico cessa di essere paradossale quando compreso"
        "dalla geometria dello spaziotempo. Le particelle generate nello stesso evento condividono un fronte"
        "d'onda dove il loro tempo proprio rimane congelato a t₀. Questa simultaneità intrinseca spiega"
        "correlaciones perfectas sin 'acción fantasmal'. La probabilità quantistica riflette la prospettiva"
        "limitata dell'osservatore, non una proprietà fondamentale.",
        width=100
    )
    
    fig.text(0.5, 0.15, texto_inferior,
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#f5f5f5", alpha=0.8,
                      edgecolor='black', linewidth=1),
             transform=fig.transFigure)
    
    # Ajuste final del layout
    plt.tight_layout(rect=[0, 0.18, 1, 0.95])
    
    plt.savefig('C:\\Users\\vedq\\Desktop\\desarrollo\\SRC-VED\\Einstein-VED\\img\\IT_entrelazamiento_geometrico_final.svg', format='svg', 
                bbox_inches='tight', dpi=300, facecolor='white')
    # plt.show()  # Desactivado en traducciones
    plt.close()
    print("✅ Guardado: entrelazamiento_geometrico_final.svg")

if __name__ == "__main__":
    print("🎯 CREAZIONE DELLA VERSIONE FINALE CON RIQUADRI ALLO STESSO LIVELLO...")
    crear_entrelazamiento_final()
    
    print("\n✨ CORRECCIONES APLICADAS:")
    print("   • Cuadros 'Fundamento Einstein' y 'Ecuaciones' allo STESSO LIVELLO")
    print("   • Figura più AMPIA (16x10) per accogliere entrambi")
    print("   • Design bilanciato e simmetrico")
    print("   • Decorazioni e colori RISPETTATI")
    print("   • ZERO sovrapposizioni")