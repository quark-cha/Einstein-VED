import numpy as np
import matplotlib.pyplot as plt

# Valores discretos de n
n_vals = np.arange(1, 21)  # n=1..20
# Longitudes de onda continuas asociadas a masas distintas (valores arbitrarios)
lambda_vals = 1 / (0.5 + 0.1*np.random.rand(len(n_vals)))

plt.figure(figsize=(10,6))

# Dibujar puntos discretos de n (modos completos)
plt.scatter(n_vals, lambda_vals, color='blue', s=100, label=r'Modos enteros $n \in \mathbb{Z}^+$')

# Añadir líneas verticales para mostrar que n es discreto
for n, lam in zip(n_vals, lambda_vals):
    plt.vlines(n, 0, lam, color='blue', alpha=0.3, linestyle='--')

# Añadir flechas mostrando que lambda puede variar continuamente
plt.arrow(5, 0.2, 0, 0.3, head_width=0.3, head_length=0.05, color='red', label=r'$\lambda$ continua')
plt.text(5.5, 0.35, 'λ continua según masa', color='red', fontsize=10)

plt.xlabel('Número de ciclos enteros n')
plt.ylabel('Longitud de onda λ')
plt.title('Confinamiento cuantizado: solo n enteros generan modos estables')
plt.xticks(n_vals)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig("figura_n_discreto_lambda_continua.png", dpi=300)
plt.show()
