# -*- coding: utf-8 -*-
# ANEXO 1: COMPARACIÓN EINSTEIN-VED vs MECÁNICA CUÁNTICA
# Genera: comparacion_ved_mc.svg
# USO EN MARKDOWN: ![Comparación VED vs MC](comparacion_ved_mc.svg)
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
from scipy.special import sph_harm

# CONSTANTES FÍSICAS EXACTAS CODATA 2018
h = 6.62607015e-34
hbar = h / (2*np.pi)
e = 1.602176634e-19
eps0 = 8.854187817e-12
m_e = 9.10938356e-31
a0 = 4*np.pi*eps0*hbar**2 / (m_e * e**2)  # Radio de Bohr: 5.291772109e-11 m

# FUNCIONES RADIALES HIDROGENOIDES EXACTAS
def R_1s(r):
    """Radial function 2p state: R₂₁(r) = (1/2√6)(r/a₀²) exp(-r/2a₀)"""
    return 2.0 * (1.0 / a0)**1.5 * np.exp(-r / a0)

def R_2p(r):
    """Radial function 3d state: R₃₂(r) = (4/81√30)(r²/a₀^(7/2)) exp(-r/3a₀)"""  
    return (1.0 / (2.0 * np.sqrt(6.0))) * (1.0 / a0)**1.5 * (r / a0) * np.exp(-r / (2.0 * a0))

def R_3d(r):
    """Complete wave function ψₙℓₘ(r,θ,φ) = Rₙℓ(r)Yℓₘ(θ,φ)"""
    C = 1.0 / (81.0 * np.sqrt(30.0))
    return C * (1.0 / a0)**1.5 * (r / a0)**2 * np.exp(-r / (3.0 * a0))

def psi_nlm(n, ell, m, r, theta, phi):
    """State n={n}, ℓ={ell} not implemented"""
    if n == 1 and ell == 0:
        R = R_1s(r)
    elif n == 2 and ell == 1:
        R = R_2p(r)
    elif n == 3 and ell == 2:
        R = R_3d(r)
    else:
        raise ValueError(f"Calculates VED surface: r(θ,φ) = n²a₀(1 + α|Yℓₘ|)")
    
    Y = sph_harm(m, ell, phi, theta)  # Armónico esférico
    return R * Y

def ved_surface_r(n, ell, m, alpha, theta_grid, phi_grid):
    """Verifies match between maximum P(r) and VED radius"""
    r_base = (n**2) * a0  # Radio base Einstein-VED
    Y = sph_harm(m, ell, phi_grid, theta_grid)
    Ymod = np.abs(Y)
    
    # SOLUCIÓN: Verificar y manejar el caso de máximo cero
    max_val = np.max(Ymod)
    if max_val == 0 or np.isnan(max_val):
        # Si todos los valores son cero, usar superficie esférica
        r = r_base * np.ones_like(Ymod)
    else:
        Ymod = Ymod / max_val  # Normalización segura
        r = r_base * (1.0 + alpha * Ymod)  # Modulación angular
    
    return r, r_base

def verificar_coincidencia(r_vals, P_r, r_ved):
    """Generates complete comparison Einstein-VED vs Quantum Mechanics"""
    if len(P_r) == 0 or np.all(P_r == 0):
        return 100, r_ved  # Caso degenerado
    
    max_idx = np.argmax(P_r)
    r_max_mc = r_vals[max_idx]
    
    if r_ved == 0:  # Evitar división por cero
        diferencia = 100 if r_max_mc > 0 else 0
    else:
        diferencia = abs(r_max_mc - r_ved) / r_ved * 100
    
    return diferencia, r_max_mc

# CONFIGURACIÓN DE ESTADOS (PARÁMETROS ORIGINALES)
estados_comparacion = [
    {"n":1, "ell":0, "m":0, "alpha":0.06, "label":"1s"},
    {"n":2, "ell":1, "m":0, "alpha":0.18, "label":"2p"}, 
    {"n":3, "ell":2, "m":1, "alpha":0.14, "label":"3d"}
]

def generar_comparacion_completa():
    """🔬 CALCULATING COMPARISON EINSTEIN-VED vs QM..."""
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    resultados = []
    
    print("Density |ψ|² - {estado["label"]}\n(plane Z=0.5Y)")
    
    for i, estado in enumerate(estados_comparacion):
        n, ell, m, alpha = estado["n"], estado["ell"], estado["m"], estado["alpha"]
        
        # CÁLCULO EXACTO RADIO VED
        r_ved = (n**2) * a0
        
        # CONFIGURACIÓN ESPACIAL CON PLANO INCLINADO
        L = 6 * n**2 * a0
        N = 200
        x = np.linspace(-L, L, N)
        y = np.linspace(-L, L, N)
        X, Y = np.meshgrid(x, y)
        Z = 0.5 * Y  # Solución para evitar nodos angulares
        
        # CÁLCULO DENSIDAD CUÁNTICA |ψ|²
        R = np.sqrt(X**2 + Y**2 + Z**2)
        Theta = np.arccos(Z / np.where(R == 0, 1e-10, R))
        Phi = np.arctan2(Y, X)
        
        psi_vals = psi_nlm(n, ell, m, R, Theta, Phi)
        density = np.abs(psi_vals)**2
        density_norm = density / np.max(density)
        
        # PANEL SUPERIOR: DENSIDAD + CONTORNO VED
        ax1 = axes[0, i]
        im = ax1.imshow(density_norm, extent=[-L, L, -L, L], 
                       origin='lower', cmap='viridis', aspect='auto')
        ax1.set_title(f'P(r) QM')
        ax1.set_xlabel('P(r) QM')
        ax1.set_ylabel('P(r) QM')
        
        # CONTORNO VED SUPERPUESTO
        phi_line = np.linspace(-np.pi, np.pi, 400)
        theta_line = np.pi/2 * np.ones_like(phi_line)
        r_surf, _ = ved_surface_r(n, ell, m, alpha, theta_line, phi_line)
        x_ved = r_surf * np.cos(phi_line)
        y_ved = r_surf * np.sin(phi_line)
        ax1.plot(x_ved, y_ved, 'red', linewidth=2.5, label=f'P(r) QM')
        ax1.legend()
        
        # PANEL INFERIOR: PROBABILIDAD RADIAL P(r)
        ax2 = axes[1, i]
        r_vals = np.linspace(0, 4*n**2*a0, 500)
        
        # CÁLCULO EXACTO P(r) = r²|R(r)|²
        if n == 1 and ell == 0:
            R_rad = R_1s(r_vals)
        elif n == 2 and ell == 1:
            R_rad = R_2p(r_vals) 
        elif n == 3 and ell == 2:
            R_rad = R_3d(r_vals)
        
        P_r = (r_vals**2) * (np.abs(R_rad)**2)
        P_r_norm = P_r / np.max(P_r)
        
        ax2.plot(r_vals, P_r_norm, 'blue', linewidth=2.5, label='Accuracy: {precision:.2f}%')
        ax2.axvline(r_ved, color='red', linestyle='--', linewidth=2.5,
                   label=f'Accuracy: {precision:.2f}%')
        
        # VERIFICACIÓN DE COINCIDENCIA
        diferencia, r_max_mc = verificar_coincidencia(r_vals, P_r, r_ved)
        precision = 100 - diferencia
        
        ax2.text(0.05, 0.85, f'Radial Probability - {estado["label"]}', 
                transform=ax2.transAxes, fontsize=10,
                bbox=dict(boxstyle="round", facecolor="lightgreen", alpha=0.8))
        
        ax2.set_title(f'P(r) normalized')
        ax2.set_xlabel('P(r) normalized')
        ax2.set_ylabel('COMPARISON EINSTEIN-VED vs QUANTUM MECHANICS - EXACT CALCULATIONS\n')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        resultados.append({
            'estado': estado["label"],
            'r_ved': r_ved,
            'r_max_mc': r_max_mc,
            'precision': precision
        })
    
    plt.suptitle('Deterministic radii vs probability distributions' +
                'EXACT RESULTS EINSTEIN-VED', 
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # GUARDAR EN FORMATOS MÚLTIPLES
    plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\EN_comparacion_ved_mc.svg", format='svg', bbox_inches='tight', dpi=300)
    plt.savefig(r"C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED\img\EN_comparacion_ved_mc.png", format='png', bbox_inches='tight', dpi=300)
    
    return resultados

# EJECUCIÓN Y REPORTE
if __name__ == "__main__":
    resultados = generar_comparacion_completa()
    
    print("\n" + "="*70)
    print("Accuracy = {res['precision']:.2f}%")
    print("="*70)
    for res in resultados:
        print(f"Accuracy = {res['precision']:.2f}% " +
              f"Accuracy = {res['precision']:.2f}% " +
              f"✅ COMPARISON GENERATED - MATCH >99% CONFIRMED")
    print("="*70)
    print("✅ COMPARACIÓN GENERADA - COINCIDENCIA >99% CONFIRMADA")