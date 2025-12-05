## Aclaraciones complementarias a la teoría Einstein-VED

Este documento proporciona una base matemática para entender los conceptos de esta teoría.
Pretendo exponer las bases matemáticas más elementales que se necesitan conocer para entender este trabajo.
Eso incluye conceptos básicos de álgebra y teoría de conjuntos al alcance de cualquier persona con un mínimo de cultura matemática, no con la intención de hacer un texto confuso sino que pueda ser comprobada la rigurosidad de mis afirmaciones.
Es por ello que es preciso exponer con brevedad conceptos básicos como el **diferencial**, el **límite** y las **transformaciones de Lorentz**, que dan lugar a esta extensión de la teoría de la relatividad espacial de Einstein.

Con esta base podrá entenderse mejor mi teoría Einstein-VED.

[La teoría que reconciliará la Mecánica Cuántica con la Relatividad de Einstein (PDF en español)](https://estradad.es/teorias/pdf/ES_Teoria_Einstein-VED.pdf)

* [Registro en Zenodo](https://zenodo.org/records/17203234)
* [ORCID](https://orcid.org/0000-0001-9942-1021)
* [Licencia](https://estradad.es/licencia.php)
* [Web](https://estradad.es)

---

### 1. Conexión entre Matemáticas y Naturaleza

Veo una conexión profunda entre las matemáticas y las leyes que definen la naturaleza.
A través de la **teoría de números** podemos acotar y describir las reglas que rigen el universo.

Primero, pensemos en la materia:
aunque el universo contuviera infinitas partículas, ese conjunto seguiría siendo **numerable**.
En otras palabras, cada partícula podría corresponder a un número natural:

> n ∈ ℕ

Por tanto, la materia está sujeta a las propiedades de los números naturales.

---

### 2. Continuidad del Espacio-Tempo

La naturaleza también muestra continuidad: entre dos instantes o dos puntos siempre hay otro intermedio.
Si tomamos dos números reales t₀ y t₁, siempre existe un número t tal que:

> t₀ < t < t₁

Y esto vale aunque t₀ y t₁ estén tan próximos como queramos.
De aquí nace el concepto de **diferencial**.

Cuando consideramos la diferencia Δt = t₁ − t₀,
y hacemos que esa cantidad sea cada vez más pequeña sin llegar a cero,
entramos en el dominio de los **infinitesimales**.
Podemos hacer Δt tan pequeño como queramos, y aún así siempre habrá otro más pequeño.
Ese proceso lleva naturalmente al concepto de **límite**.

Un límite es aquello a lo que podemos aproximarnos de manera infinita:
por muy cerca que estemos, siempre existe un valor más próximo.
Por eso, cuando en cálculo se habla de diferenciales, no se trata de dividir por cero,
sino de aproximarse a una división imposible sin realizarla realmente.

Los diferenciales nos permiten trabajar con magnitudes que tienden a cero pero que nunca son cero,
y eso nos da la base matemática de la **continuidad del espacio-tiempo**.

---

### 3. Universo como combinación de lo discreto y lo continuo

Así, tomamos **ℝ** como la representación de esa continuidad en cada dimensión.
El universo, en este sentido, puede verse como un espacio de cuatro dimensiones reales:

> ℝ⁴

que contiene un número n de partículas, con:

> n ⊂ ℕ

De esta forma, el universo combina lo **discreto** (la materia, los números naturales)
y lo **continuo** (el espacio-tiempo, los números reales).
Ambos se relacionan a través de los conceptos de **límite**, **diferencial** y **continuidad**,
que también se reflejan en las **leyes de Lorentz** y en la **estructura de la física moderna**.

---

### 4. Demostración: Partículas en un espacio-tiempo propio en el origen del frente de onda

**Enunciado.**
Bajo las hipótesis del marco Einstein-VED, una partícula asociada a un modo localizado cuyo máximo está en el punto (O) de un frente de onda nulo puede ser interpretada como embebida en un **espacio-tiempo propio** centrado en (O).
Además, un observador que intercepta el frente de onda en (O) mide intervalos propios que tienden a cero cuando considera eventos cada vez más próximos sobre la hipersuperficie del frente:

$$
dt' \to 0, \quad ds' \to 0.
$$

#### Hipótesis

1. ((\mathcal{M}, g)) es localmente Minkowskiano.
2. Existe una hipersuperficie de frente de onda nula (\mathcal{N} = {x \in \mathcal{M} : \Phi(x) = 0}) con gradiente nulo:
   $$g^{\mu\nu}\partial_\mu\Phi,\partial_\nu\Phi = 0 \text{ en } \mathcal{N}.$$
3. La partícula (p_n) está representada por un modo (\psi_n(x) = \phi_n(x)e^{-i\omega t}) con soporte efectivo contenido en una región (U_n) que contiene un punto distinguido (O \in \mathcal{N}).
4. El observador usa coordenadas locales (x'^\mu) que interceptan (\mathcal{N}) en (O).

#### Demostración

1. **Naturaleza nula del frente:**
   Para dos eventos infinitesimales vecinos sobre (\mathcal{N}), se cumple:
   $$ds^2 = g_{\mu\nu} dx^\mu dx^\nu = 0.$$
   Es decir, las separaciones entre puntos de (\mathcal{N}) son de tipo luz.

2. **Invariancia Lorentziana local:**
   Bajo una transformación local Lorentz (x'^\mu = \Lambda^\mu{}*\nu x^\nu + a^\mu), la condición (ds^2 = 0) se conserva:
   $$ds'^2 = g'*{\mu\nu} dx'^\mu dx'^\nu = ds^2 = 0.$$

3. **Intervalo propio y tiempo propio:**
   El intervalo propio entre dos eventos infinitesimales es:
   $$d\tau^2 = ds'^2.$$
   Para eventos sobre (\mathcal{N}): (d\tau^2 = 0), por tanto, el tiempo propio entre ellos se anula.

4. **Límite de aproximación del observador:**
   Si el observador considera eventos cada vez más próximos en (\mathcal{N}) y se aproxima a (O):
   $$dx'^\mu \to 0 \quad \Rightarrow \quad dt' \to 0, \ ds'^2 \to 0.$$
   Por tanto, el tiempo propio entre ellos tiende a cero en el límite.

5. **Interpretación física:**
   La partícula (p_n), como modo con soporte efectivo centrado en (O), tiene su dinámica interna ligada al frente.
   Para un observador que intercepta el frente en (O), las transiciones asociadas estrictamente a la superficie nula aparecen con intervalos propios nulos.
   Esto justifica la descripción de un **espacio-tiempo propio concentrado en (O)**.

#### Observaciones

* La demostración se limita a eventos sobre la hipersuperficie nula; no implica ausencia de evolución física: la dinámica puede requerir eventos ligeramente fuera de (\mathcal{N}).
* Si el frente tiene anchura finita (\epsilon > 0), los intervalos medidos serán pequeños pero no nulos; el análisis es válido en el límite (\epsilon \to 0).
* El espacio-tiempo propio puede modelarse como una **fibración local del continuo** sobre los soportes (U_n), siendo (O) una fibra degenerada asociada al frente nulo.
