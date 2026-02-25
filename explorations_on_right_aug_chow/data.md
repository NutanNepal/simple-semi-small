# Right Augmented Chow Function

Just some random notes on the right augmented chow function.

## Definition

The **right augmented Chow function** (denoted as $F$ in `ssrec.tex`) is defined as the convolution of the Chow function ($\underline{H}$) and the reversed Kazhdan-Lusztig function ($f^{\text{rev}}$):

$$F = \underline{H} \cdot f^{\text{rev}}$$

where $f$ is the right Kazhdan-Lusztig function (typically the KL polynomial $P_M$).

### Symmetry Property Implication

The right augmented Chow function satisfies the palindromic property $F^{\text{rev}} = F$. This symmetry, combined with the definition $F = \underline{H} \cdot f^{\text{rev}}$, implies that it can also be expressed as:

$$F = \underline{H}^{\text{rev}} \cdot f$$

In terms of convolution components:
$$F(M) = \sum_{F \in L(M)} \underline{H}^{\text{rev}}(M^F) \cdot f(M_F)$$

### Convolution Formula

In the incidence algebra of the lattice of flats $L(M)$, the convolution of two functions $a$ and $b$ for an interval $[\hat{0}, \hat{1}]$ is given by the sum over flats $F \in L(M)$:

Using the following notations:
- $M^F$ for the **restriction** of $M$ to $F$.
- $M_F$ for the **contraction** of $M$ by $F$.

The right augmented Chow function $F(M)$ is:

$$F(M) = \sum_{F \in L(M)} \underline{H}(M^F) \cdot f^{\text{rev}}(M_F)$$

Expanding the rev operator:

$$F(M) = \sum_{F \in L(M)} \underline{H}(M^F) \cdot x^{\text{rk}(M_F)} f(M_F)(x^{-1})$$

### Results and Conjectures

1.  **Conjecture $F(M) = G(M)$**:
    *   Verified for small matroids like $K_2, K_3$ and small uniform matroids.
    *   **Discrepancy found for $K_4$**: 
        *   $F(K_4) = 1 + 15x + 15x^2 + x^3$
        *   $G(K_4) = 1 + 14x + 15x^2 + x^3$ (using $G = f^{\text{rev}} \cdot \underline{H}$)
        *   The discrepancy is exactly $x$.
    *   This suggests that the symmetry $F=G$ might depend on specific properties or a different definition of $G$.

2.  **Map on KL Basis**:
    *   The map $\Psi: s \mapsto x^{\text{rk}(s)} \underline{H}^{\text{rev}}(M^s)(x^{-2})$ takes the KL basis element $\text{kl}^t$ to $x^{\text{rk}(t)} F(M^t)(x^{-2})$.
    *   This identity has been verified computationally for $K_n$ and the Fano matroid in the research notebook.

## Implementation in SageMath

The notebook `examples/convolutionsF.ipynb` provides the relevant functions. Note that the notebook uses `delete(E - F)` for restriction ($M^F$) and `contract(F)` for contraction ($M_F$):

```python
def convolve(f, g, M):
    E = M.groundset()
    flats = list(M.lattice_of_flats())
    sum = P(0)
    for F in flats:
        # Restriction M^F is M.delete(E - F)
        # Contraction M_F is M.contract(F)
        sum += f(M.delete(E - F))(x) * g(M.contract(F))(x)
    return sum

# Mapping functions
kl_poly = lambda M: M.lattice_of_flats().kazhdan_lusztig_polynomial()(x)
klpoly_rev = lambda M: kl_poly(M)(x**-1) * x**M.rank()
chow = chow_polynomial

# Computing Right Augmented Chow
right_aug_chow = convolve(chow, klpoly_rev, M)
```

## Symmetry Properties

The right augmented Chow function satisfies:
$$F_{st}(x) = x^{\rho_{st}} F_{st}(x^{-1})$$
where $\rho_{st} = \text{rk}(t) - \text{rk}(s)$. For the whole matroid, it's palindromic with respect to the rank.
