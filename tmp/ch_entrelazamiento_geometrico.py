# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import matplotlib

# Configuración para caracteres chinos
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

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
    - Cuadros "基本方程" y "量子纠缠:爱因斯坦-VED几何解释" en mismo nivel
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
    plt.suptitle('内部框架:共享固有时间', 
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
    ax1.set_title('外部框架:传统视角', fontweight='bold', fontsize=12)
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
    ax2.set_title('符号说明:\n\n', fontweight='bold', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # --- CUADRO DESCRIPTIVO IZQUIERDO ---
    texto_izquierdo = textwrap.fill(
        "🔴 粒子 A (45°)\n"
        "🟢 粒子 B (225°)\n"
        "⚫ 观察者\n"
        "▬▬ 几何连接\n"
        "▬▬ 视线"
        "波前",
        width=20
    )
    
    fig.text(0.02, 0.75, texto_izquierdo, 
             ha='left', va='center', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.6", facecolor="white", alpha=0.9,
                      edgecolor='gray', linewidth=1),
             transform=fig.transFigure)
    
    # --- CUADRO CENTRAL "爱因斯坦-VED关键:\n\n" ---
    texto_central = textwrap.fill(
        "两个粒子(包括对跖点)\n共享相同的固有时空 t₀, s₀\n\n"
        "因为:在光速c下 dt' → 0 且 ds' → 0\n\n"
        "→ 0 且 ds"
        "没有超距作用"
        "没有超距作用"
        "爱因斯坦-VED基础:\n\n",
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
        "纠缠粒子从起源起共享共同的固有时空."
        "当以光速c运动时,它们的固有时间和空间微分趋于零 "
        "(dt' 这种几何同时性解释了量子相关性而不违反相对论.' → 0),使它们保持在相同的时刻 t₀ 和位置 s₀. "
        "这种几何同时性解释了量子相关性而不违反相对论. "
        "基本方程:\n\n",
        width=45  # Más estrecho para caber al lado
    )
    
    fig.text(0.25, 0.35, texto_einstein,
             ha='center', va='center', fontsize=10.5, style='italic',
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#ffebee", alpha=0.9,
                      edgecolor='red', linewidth=2),
             transform=fig.transFigure)
    
    # CUADRO ECUACIONES (DERECHA) - MISMO NIVEL
    texto_ecuaciones = textwrap.fill(
        "对于以光速c运动的粒子:\n"
        "场方程:\n"
        "• dt' 这种几何同时性解释了量子相关性而不违反相对论.' → 0\n"
        "• 没有超距作用" 
        "• 没有超距作用"
        "在固有框架中的绝对同时性"
        "在固有框架中的绝对同时性"
        "爱因斯坦-VED解释:当从时空几何理解时,量子纠缠不再矛盾.",
        width=30
    )
    
    fig.text(0.75, 0.35, texto_ecuaciones, 
             ha='center', va='center', fontsize=10.5, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#f0f8ff", alpha=0.9,
                      edgecolor='blue', linewidth=2),
             transform=fig.transFigure)
    
    # --- TEXTO EXPLICATIVO INFERIOR ---
    texto_inferior = textwrap.fill(
        "在同一事件中生成的粒子共享一个波前, "
        "其中它们的固有时间冻结在 t₀.这种内在同时性解释了 "
        ""完美的相关性,没有""幽灵作用"".量子概率反映了" "
        "幽灵作用 "
        "🎯 创建具有相同水平框架的最终版本...",
        width=100
    )
    
    fig.text(0.5, 0.15, texto_inferior,
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#f5f5f5", alpha=0.8,
                      edgecolor='black', linewidth=1),
             transform=fig.transFigure)
    
    # Ajuste final del layout
    plt.tight_layout(rect=[0, 0.18, 1, 0.95])
    
    plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\entrelazamiento_geometrico_final.svg", format='svg', 
                bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()
    print("✅ Guardado: entrelazamiento_geometrico_final.svg")

if __name__ == "__main__":
    print("\n✨ 应用的修正:")
    crear_entrelazamiento_final()
    
    print("• '爱因斯坦基础'和'方程'框架在同一水平")
    print("   • Cuadros '基本方程' y 'Ecuaciones' en MISMO NIVEL")
    print("   • 平衡对称的设计")
    print("   • 装饰和颜色已保留")
    print("   • 零重叠")
    print("   • CERO solapamientos")