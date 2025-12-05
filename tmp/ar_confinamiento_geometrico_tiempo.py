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

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# =============================================================================
# GRÁFICA 1: n=1 - Estado Fundamental (Tubo liso + círculo)
# =============================================================================
def grafica1_n1_fundamental():
    """n=1: أنبوب زمكان أملس + موجة دائرية أساسية"""
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    radio_base = 1.5
    delta_t = 8
    
    # Tubo liso del espacio-tiempo
    z = np.linspace(0, delta_t, 80)
    theta = np.linspace(0, 2 * np.pi, 80)
    Z, Theta = np.meshgrid(z, theta)
    
    X = radio_base * np.cos(Theta)
    Y = radio_base * np.sin(Theta)
    
    ax.plot_surface(X, Y, Z, 
                   color='lightblue',
                   alpha=0.15,
                   rstride=2, cstride=2,
                   linewidth=0)
    
    # Onda circular fundamental (n=1)
    z_medio = delta_t / 2
    theta_circ = np.linspace(0, 2 * np.pi, 100)
    X_circ = radio_base * np.cos(theta_circ)
    Y_circ = radio_base * np.sin(theta_circ)
    Z_circ = z_medio * np.ones_like(theta_circ)
    
    ax.plot(X_circ, Y_circ, Z_circ, 'red', linewidth=4, alpha=0.9)
    
    ax.set_axis_off()
    ax.view_init(elev=20, azim=-60)
    ax.set_title('الحالة الأساسية n=1\nالزمكان + موجة دائرية', 
                fontweight='bold', pad=20, fontsize=12)
    
    plt.tight_layout()
    plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\AR_1_n1_fundamental.svg", bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()
    print("✅ 1_n1_fundamental.svg")

# =============================================================================
# GRÁFICA 2: n=3 - Estado Excitado (Variedad + 3 nodos)
# =============================================================================
def grafica2_n3_excitado():
    """n=3: متعدد الزمكان + موجة ذات 3 عقد"""
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    radio_base = 1.5
    delta_t = 8
    
    # Variedad del espacio-tiempo (n=3)
    z = np.linspace(0, delta_t, 150)
    theta = np.linspace(0, 2 * np.pi, 150)
    Z, Theta = np.meshgrid(z, theta)
    
    wave_superficie = 0.2 * np.sin(3 * Theta)
    R_superficie = radio_base + wave_superficie
    X = R_superficie * np.cos(Theta)
    Y = R_superficie * np.sin(Theta)
    
    ax.plot_surface(X, Y, Z, 
                   facecolors=cm.viridis((wave_superficie + 0.2)/0.4),
                   alpha=0.6,
                   rstride=3, cstride=3,
                   linewidth=0)
    
    # Onda con 3 nodos (n=3)
    z_medio = delta_t / 2
    theta_onda = np.linspace(0, 2 * np.pi, 200)
    wave_onda = 0.25 * np.sin(3 * theta_onda)
    R_onda = radio_base + wave_onda
    X_onda = R_onda * np.cos(theta_onda)
    Y_onda = R_onda * np.sin(theta_onda)
    Z_onda = z_medio * np.ones_like(theta_onda)
    
    ax.plot(X_onda, Y_onda, Z_onda, 'red', linewidth=5, alpha=0.9)
    
    ax.set_axis_off()
    ax.view_init(elev=20, azim=-60)
    ax.set_title('الحالة المستثارة n=3\nمتعدد الزمكان + 3 عقد', 
                fontweight='bold', pad=20, fontsize=12)
    
    plt.tight_layout()
    plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\AR_2_n3_excitado.svg", bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()
    print("✅ 2_n3_excitado.svg")

# =============================================================================
# GRÁFICA 3: Comparación n=1 vs n=3
# =============================================================================
def grafica3_comparacion():
    """مقارنة جنبًا إلى جنب n=1 مقابل n=3"""
    
    fig = plt.figure(figsize=(16, 7))
    
    radio_base = 1.2
    delta_t = 6
    
    # ===== n=1 =====
    ax1 = fig.add_subplot(121, projection='3d')
    
    z = np.linspace(0, delta_t, 60)
    theta = np.linspace(0, 2 * np.pi, 60)
    Z, Theta = np.meshgrid(z, theta)
    
    X1 = radio_base * np.cos(Theta)
    Y1 = radio_base * np.sin(Theta)
    
    ax1.plot_surface(X1, Y1, Z, color='lightblue', alpha=0.2, rstride=2, cstride=2, linewidth=0)
    
    z_medio = delta_t / 2
    theta_circ = np.linspace(0, 2 * np.pi, 100)
    X_circ = radio_base * np.cos(theta_circ)
    Y_circ = radio_base * np.sin(theta_circ)
    ax1.plot(X_circ, Y_circ, z_medio * np.ones_like(theta_circ), 'red', linewidth=3)
    
    ax1.set_axis_off()
    ax1.view_init(elev=20, azim=-60)
    ax1.set_title('n=1: الحالة الأساسية', fontweight='bold', pad=15)
    
    # ===== n=3 =====
    ax2 = fig.add_subplot(122, projection='3d')
    
    wave_n3 = 0.15 * np.sin(3 * Theta)
    R_n3 = radio_base + wave_n3
    X2 = R_n3 * np.cos(Theta)
    Y2 = R_n3 * np.sin(Theta)
    
    ax2.plot_surface(X2, Y2, Z, facecolors=cm.plasma((wave_n3 + 0.15)/0.3),
                    alpha=0.5, rstride=2, cstride=2, linewidth=0)
    
    wave_onda = 0.2 * np.sin(3 * theta_circ)
    R_onda = radio_base + wave_onda
    X_onda = R_onda * np.cos(theta_circ)
    Y_onda = R_onda * np.sin(theta_circ)
    ax2.plot(X_onda, Y_onda, z_medio * np.ones_like(theta_circ), 'red', linewidth=4)
    
    ax2.set_axis_off()
    ax2.view_init(elev=20, azim=-60)
    ax2.set_title('n=3: الحالة المستثارة', fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\AR_3_comparacion_n1_n3.svg", bbox_inches='tight', dpi=300, facecolor='white')
    
    plt.close()
    print("✅ 3_comparacion_n1_n3.svg")

# =============================================================================
# GRÁFICA 4: Generación por curvas dt (n=1)
# =============================================================================
def grafica4_generacion_dt_n1():
    """يظهر كيف تنشئ منحنيات dt السطح n=1"""
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    radio_base = 1.5
    delta_t = 8
    
    # Superficie generada
    z = np.linspace(0, delta_t, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    Z, Theta = np.meshgrid(z, theta)
    
    X = radio_base * np.cos(Theta)
    Y = radio_base * np.sin(Theta)
    
    ax.plot_surface(X, Y, Z, color='lightblue', alpha=0.15, rstride=2, cstride=2, linewidth=0)
    
    # Múltiples curvas dt
    niveles_dt = 5
    for i, altura in enumerate(np.linspace(1, delta_t-1, niveles_dt)):
        theta_curva = np.linspace(0, 2 * np.pi, 100)
        X_curva = radio_base * np.cos(theta_curva)
        Y_curva = radio_base * np.sin(theta_curva)
        Z_curva = altura * np.ones_like(theta_curva)
        
        alpha = 0.8 if i == niveles_dt//2 else 0.4
        linewidth = 3 if i == niveles_dt//2 else 1.5
        ax.plot(X_curva, Y_curva, Z_curva, 'red', linewidth=linewidth, alpha=alpha)
    
    # Flecha δt
    ax.plot([radio_base+0.3, radio_base+0.3], [0, 0], [0, delta_t], 
           'green', linewidth=3, linestyle='--', alpha=0.7)
    ax.scatter([radio_base+0.3], [0], [delta_t], color='green', s=50, marker='^')
    ax.text(radio_base+0.5, 0, delta_t/2, 'δt', color='green', fontsize=12, fontweight='bold')
    
    ax.set_axis_off()
    ax.view_init(elev=20, azim=-60)
    ax.set_title('توليد n=1: dt → سطح\nمنحنيات دائرية تولد أسطوانة', 
                fontweight='bold', pad=20, fontsize=12)
    
    plt.tight_layout()
    plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\AR_4_generacion_dt_n1.svg", bbox_inches='tight', dpi=300, facecolor='white')
    
    plt.close()
    print("✅ 4_generacion_dt_n1.svg")

# =============================================================================
# GRÁFICA 5: Generación por curvas dt (n=3)
# =============================================================================
def grafica5_generacion_dt_n3():
    """يظهر كيف تنشئ منحنيات dt السطح n=3"""
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    radio_base = 1.5
    delta_t = 8
    
    # Superficie generada
    z = np.linspace(0, delta_t, 150)
    theta = np.linspace(0, 2 * np.pi, 150)
    Z, Theta = np.meshgrid(z, theta)
    
    wave_superficie = 0.2 * np.sin(3 * Theta)
    R_superficie = radio_base + wave_superficie
    X = R_superficie * np.cos(Theta)
    Y = R_superficie * np.sin(Theta)
    
    ax.plot_surface(X, Y, Z, facecolors=cm.viridis((wave_superficie + 0.2)/0.4),
                   alpha=0.3, rstride=3, cstride=3, linewidth=0)
    
    # Múltiples curvas dt
    niveles_dt = 5
    for i, altura in enumerate(np.linspace(1, delta_t-1, niveles_dt)):
        theta_curva = np.linspace(0, 2 * np.pi, 200)
        wave_curva = 0.25 * np.sin(3 * theta_curva)
        R_curva = radio_base + wave_curva
        X_curva = R_curva * np.cos(theta_curva)
        Y_curva = R_curva * np.sin(theta_curva)
        Z_curva = altura * np.ones_like(theta_curva)
        
        alpha = 0.9 if i == niveles_dt//2 else 0.4
        linewidth = 4 if i == niveles_dt//2 else 1.5
        ax.plot(X_curva, Y_curva, Z_curva, 'red', linewidth=linewidth, alpha=alpha)
    
    # Flecha δt
    ax.plot([radio_base+0.8, radio_base+0.8], [0, 0], [0, delta_t], 
           'green', linewidth=3, linestyle='--', alpha=0.7)
    ax.scatter([radio_base+0.8], [0], [delta_t], color='green', s=50, marker='^')
    ax.text(radio_base+1.0, 0, delta_t/2, 'δt', color='green', fontsize=12, fontweight='bold')
    
    ax.set_axis_off()
    ax.view_init(elev=20, azim=-60)
    ax.set_title('توليد n=3: dt → متعدد\nمنحنيات مع عقد تولد هندسة', 
                fontweight='bold', pad=20, fontsize=12)
    
    plt.tight_layout()
    plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\AR_5_generacion_dt_n3.svg", bbox_inches='tight', dpi=300, facecolor='white')
    
    plt.close()
    print("✅ 5_generacion_dt_n3.svg")

# =============================================================================
# GRÁFICA 6: Evolución Temporal Completa
# =============================================================================
def grafica6_evolucion_temporal():
    """تطور كامل dt عبر δt"""
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    radio_base = 1.5
    delta_t = 10
    
    # Superficie de fondo
    z = np.linspace(0, delta_t, 200)
    theta = np.linspace(0, 2 * np.pi, 200)
    Z, Theta = np.meshgrid(z, theta)
    
    wave_superficie = 0.15 * np.sin(3 * Theta)
    R_superficie = radio_base + wave_superficie
    X = R_superficie * np.cos(Theta)
    Y = R_superficie * np.sin(Theta)
    
    ax.plot_surface(X, Y, Z, facecolors=cm.plasma((wave_superficie + 0.15)/0.3),
                   alpha=0.15, rstride=4, cstride=4, linewidth=0)
    
    # Curvas dt en diferentes δt
    tiempos = [2, 4, 6, 8]
    for i, t in enumerate(tiempos):
        theta_curva = np.linspace(0, 2 * np.pi, 200)
        wave_curva = 0.2 * np.sin(3 * theta_curva)
        R_curva = radio_base + wave_curva
        X_curva = R_curva * np.cos(theta_curva)
        Y_curva = R_curva * np.sin(theta_curva)
        Z_curva = t * np.ones_like(theta_curva)
        
        color = 'red' if i % 2 == 0 else 'darkred'
        ax.plot(X_curva, Y_curva, Z_curva, color, linewidth=3, alpha=0.8)
        ax.text(0, -radio_base-0.3, t, f'δt={t}', ha='center', fontweight='bold',
               bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    
    # Evolución temporal
    ax.plot([radio_base+0.5, radio_base+0.5], [0, 0], [1, delta_t-1], 
           'blue', linewidth=4, alpha=0.8)
    ax.scatter([radio_base+0.5], [0], [delta_t-1], color='blue', s=100, marker='^')
    ax.text(radio_base+0.7, 0, delta_t/2, 'تطور\nزمني', color='blue', fontweight='bold')
    
    ax.set_axis_off()
    ax.view_init(elev=25, azim=-50)
    ax.set_title('تطور كامل: dt → δt → حالات n\nحصر كمي أينشتاين-VED', 
                fontweight='bold', pad=25, fontsize=14)
    
    plt.tight_layout()
    plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\AR_6_evolucion_temporal.svg", bbox_inches='tight', dpi=300, facecolor='white')
    
    plt.close()
    print("✅ 6_evolucion_temporal.svg")

# =============================================================================
# EJECUTAR LAS 6 GRÁFICAS
# =============================================================================
def main_6_graficas():
    print("🎨 يجري توليد الرسوم البيانية الـ6 الكاملة لأينشتاين-VED...")
    
    # 1. Estados fundamentales
    grafica1_n1_fundamental()
    grafica2_n3_excitado()
    grafica3_comparacion()
    
    # 2. Proceso generativo
    grafica4_generacion_dt_n1()
    grafica5_generacion_dt_n3()
    grafica6_evolucion_temporal()
    
    print("\n✅ الرسوم البيانية الـ6 الكاملة:")
    print("   1. 1_n1_fundamental.svg - Estado base")
    print("   2. 2_n3_excitado.svg - Estado excitado") 
    print("   3. 3_comparacion_n1_n3.svg - Comparación")
    print("   4. 4_generacion_dt_n1.svg - Generación n=1")
    print("   5. 5_generacion_dt_n3.svg - Generación n=3")
    print("   6. 6_evolucion_temporal.svg - Evolución completa")

if __name__ == "__main__":
    main_6_graficas()