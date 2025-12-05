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
from mpl_toolkits.mplot3d import Axes3D

# Constantes
lambda_e = 2.426310238e-12  # Longitud de onda Compton del electrón (m)
a0 = 0.529e-10              # Radio de Bohr (m)

# Número de niveles a mostrar
n_levels = 3

# Función para dibujar esferas y superficies de onda
def draw_orbital(ax, r, n_cycles, color='b', alpha=0.3, label=''):
    # Superficie esférica (aproximación conceptual)
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 50)
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color=color, alpha=alpha)
    
    # Representar la longitud de onda sobre la superficie
    # Se muestra como "ondas" radiales sobre la superficie
    phi = np.linspace(0, 2*np.pi, n_cycles*10)
    theta = np.pi/2 + 0.1*np.sin(n_cycles*phi)  # ligera ondulación
    x_wave = r * np.cos(phi) * np.sin(theta)
    y_wave = r * np.sin(phi) * np.sin(theta)
    z_wave = r * np.cos(theta)
    ax.plot3D(x_wave, y_wave, z_wave, color=color, alpha=0.8, linewidth=1)

# Crear figura 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Hydrogen Orbitals with confined wave (Einstein-VED)")

colors = ['b', 'g', 'r']
for n in range(1, n_levels+1):
    r_n = a0 * n
    n_cycles = 137 * n
    draw_orbital(ax, r_n, n_cycles, color=colors[n-1], alpha=0.2, label=f'n={n}, {n_cycles} λ')

ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.set_zlabel("Z [m]")
ax.legend()
plt.show()
