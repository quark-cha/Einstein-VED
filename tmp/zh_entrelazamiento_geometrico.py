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
idioma_actual = "zh"   # definido por el generador del temporal

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
    plt.suptitle('量子纠缠：爱因斯坦-VED几何解释', 
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
    ax1.set_title('内部框架：共享的固有时', fontweight='bold', fontsize=12)
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
    ax2.set_title('外部框架：传统视角', fontweight='bold', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # --- CUADRO DESCRIPTIVO IZQUIERDO ---
    texto_izquierdo = textwrap.fill(
        "符号体系：\n\n"
        "🔴 粒子A（45°）\n"
        "🟢 粒子B（225°）\n"
        "⚫ 观察者\n"
        "▬▬ 几何连接\n"
        "▬▬ 视线",
        width=20
    )
    
    fig.text(0.02, 0.75, texto_izquierdo, 
             ha='left', va='center', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.6", facecolor="white", alpha=0.9,
                      edgecolor='gray', linewidth=1),
             transform=fig.transFigure)
    
    # --- CUADRO CENTRAL "FRENTE DE ONDA" ---
    texto_central = textwrap.fill(
        "爱因斯坦-VED关键：\n\n"
        "两个粒子（包括对跖点）\n共享相同的固有时空t₀，s₀\n\n"
        "Porque: dt' → 0 y ds' → 0 在光速c下\n\n"
        "t = t₀ + dt' → t₀\n"
        "s = s₀ + ds' → s₀\n\n"
        "无超距作用",
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
        "爱因斯坦-VED基础：\n\n"
        "纠缠粒子从其起源起共享共同的固有时空。"
        "当以光速c运动时，它们的固有时间和空间微分趋于零"
        "(dt' → 0, ds' → 0），使它们保持连接在相同的时刻t₀和位置s₀。"
        "这种几何同时性解释了量子关联而不违反相对论。",
        width=45  # Más estrecho para caber al lado
    )
    
    fig.text(0.25, 0.35, texto_einstein,
             ha='center', va='center', fontsize=10.5, style='italic',
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#ffebee", alpha=0.9,
                      edgecolor='red', linewidth=2),
             transform=fig.transFigure)
    
    # CUADRO ECUACIONES (DERECHA) - MISMO NIVEL
    texto_ecuaciones = textwrap.fill(
        "基本方程：\n\n"
        "对于以光速c运动的粒子：\n"
        "• dt' → 0, ds' → 0\n"
        "• t = t₀ + dt' → t₀\n" 
        "• s = s₀ + ds' → s₀\n\n"
        "场方程：\n"
        "Gₘₙ + Λgₘₙ = (8πG/c⁴)Tₘₙ\n\n"
        "在固有坐标系中的绝对同时性",
        width=30
    )
    
    fig.text(0.75, 0.35, texto_ecuaciones, 
             ha='center', va='center', fontsize=10.5, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#f0f8ff", alpha=0.9,
                      edgecolor='blue', linewidth=2),
             transform=fig.transFigure)
    
    # --- TEXTO EXPLICATIVO INFERIOR ---
    texto_inferior = textwrap.fill(
        "爱因斯坦-VED解释：当从时空几何理解时"
        "量子纠缠不再具有悖论性。在同一事件中产生的粒子共享一个"
        "波前，其中它们的固有时保持冻结在t₀。这种内在同时性解释了"
        "correlaciones perfectas sin 'acción fantasmal'。量子概率反映了观察者的"
        "有限视角，而非基本属性。",
        width=100
    )
    
    fig.text(0.5, 0.15, texto_inferior,
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#f5f5f5", alpha=0.8,
                      edgecolor='black', linewidth=1),
             transform=fig.transFigure)
    
    # Ajuste final del layout
    plt.tight_layout(rect=[0, 0.18, 1, 0.95])
    
    plt.savefig('C:\\Users\\vedq\\Desktop\\desarrollo\\SRC-VED\\Einstein-VED\\img\\ZH_entrelazamiento_geometrico_final.svg', format='svg', 
                bbox_inches='tight', dpi=300, facecolor='white')
    # plt.show()  # Desactivado en traducciones
    plt.close()
    print("✅ Guardado: entrelazamiento_geometrico_final.svg")

if __name__ == "__main__":
    print("🎯 创建包含同级别框图的最终版本...")
    crear_entrelazamiento_final()
    
    print("\n✨ CORRECCIONES APLICADAS:")
    print("   • Cuadros 'Fundamento Einstein' y 'Ecuaciones' 在同一级别")
    print("   • 更宽的图形（16x10）以容纳两者")
    print("   • 平衡对称的设计")
    print("   • 装饰和颜色得到尊重")
    print("   • 零重叠")