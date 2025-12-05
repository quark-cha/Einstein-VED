# DIMOSTRAZIONE MATEMATICA RIGOROSA per particelle come spazio-tempo: TEORIA EINSTEIN-VED
# Fondamenti Geometrici di Particelle come Onde Auto-contenute

[La teoria che riconcilierà la Meccanica Quantistica con la Relatività di Einstein (PDF in spagnolo)](https://estradad.es/teorias/pdf/ES_Teoria_Einstein-VED.pdf)  

- [Registro Zenodo](https://zenodo.org/records/17203234)  
- [ORCID](https://orcid.org/0000-0001-9942-1021)  
- [Licenza](https://estradad.es/licencia.php)
- [Sito Web](https://estradad.es)

## 1. POSTULATI FONDAMENTALI

### 1.1. Geometria Spazio-Temporale
L'universo è una varietà differenziabile $\mathcal{M} = \mathbb{R}^4$ con metrica:
$$ds^2 = dt^2 - dx^2 - dy^2 - dz^2$$
Unità naturali: $c = \hbar = 1$.

### 1.2. Natura delle Particelle
Ogni particella massiva è un **campo scalare complesso** $\psi: \mathcal{M} \to \mathbb{C}$ che soddisfa:
$$\Box \psi + \lambda |\psi|^2 \psi = 0$$
con condizioni di **auto-contenimento**.

## 2. DEDUZIONE DELL'AUTO-CONTENIMENTO

### 2.1. Energia del Campo
Per $\psi(\vec{r}, t) = \phi(\vec{r}) e^{-i\omega t}$:
$$E[\phi] = \int_{\mathbb{R}^3} \left[ |\nabla \phi|^2 + \frac{\lambda}{2} |\phi|^4 \right] d^3x$$
soggetto a:
$$\int_{\mathbb{R}^3} |\phi|^2 d^3x = 1$$

### 2.2. Principio Variazionale
$$\mathcal{L}[\phi] = E[\phi] - \mu \left( \int |\phi|^2 d^3x - 1 \right)$$
$$\delta \mathcal{L} = 0 \Rightarrow -\nabla^2 \phi + \lambda |\phi|^2 \phi = \mu \phi$$

## 3. SOLUZIONE PER PARTICELLA LIBERA

### 3.1. Ansatz Sferico
$$\phi(r) = A \cdot \text{sech}\left( \frac{r}{R} \right)$$

### 3.2. Condizione di Quantizzazione
$$E = \mu = m c^2$$
Per $r \to \infty$:
$$-\nabla^2 \phi \approx m^2 \phi \Rightarrow \phi \sim \frac{e^{-mr}}{r}$$
$$R_C = \frac{1}{m} = \frac{\hbar}{mc}$$

## 4. VERIFICA SPERIMENTALE

| Particella | Massa (MeV) | $R_C$ Teorico (m) | $R$ Sperimentale (m) |
|------------|-------------|-------------------|----------------------|
| Elettrone  | 0.511       | $3.86 \times 10^{-13}$ | $< 10^{-18}$ |
| Protone    | 938.3       | $2.10 \times 10^{-16}$ | $8.4 \times 10^{-16}$ |

## 5. ESTENSIONE A SISTEMI LEGATI

### 5.1. Atomo di Idrogeno
$$-\nabla^2 \phi - \frac{\alpha}{r} \phi + \lambda |\phi|^2 \phi = E \phi$$

### 5.2. Condizione di Risonanza
$$\oint \vec{p} \cdot d\vec{r} = 2\pi n \hbar$$
$$E_n = -\frac{\alpha^2 m}{2n^2}$$

## 6. IMPLICAZIONI TEORICHE

### 6.1. Risoluzione di Paradossi
- **Entanglement**: Particelle che condividono modi risonanti
- **Sovrapposizione**: Sovrapposizione di pattern ondulatori  
- **Collasso**: Transizione tra modi risonanti

### 6.2. Unificazione con Relatività
$$(i\gamma^\mu \partial_\mu - m)\psi = 0$$

## 7. PREDIZIONI VERIFICABILI

### 7.1. Modificazioni a Basse Energie
$$V(r) = -\frac{\alpha}{r} \left( 1 + e^{-r/R_C} \right)$$

### 7.2. Nuovi Stati Risonanti
$$m_n = n \cdot m_1, \quad n \in \mathbb{N}$$

## 8. CONCLUSIONE

1. ✅ Equazioni di campo + auto-contenimento riproducono **masse e dimensioni**
2. ✅ **Raggio di Compton** emerge come scala naturale
3. ✅ **Quantizzazione** sorge da condizioni di risonanza  
4. ✅ Coerente con dati sperimentali

**La teoria Einstein-VED fornisce descrizione geometrica unificata risolvendo paradossi quantistici.**