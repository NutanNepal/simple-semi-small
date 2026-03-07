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

The left augmented Chow function is defined as $G = g^{\text{rev}} \cdot \underline{H}$. Here $g$ is the left Kazhdan-Lusztig function (typically the zeta function of $\mathcal{L}(M)$).

Expanding the rev operator:

$$F(M) = \sum_{F \in L(M)} \underline{H}(M^F) \cdot x^{\text{rk}(M_F)} f(M_F)(x^{-1})$$

### The Module $H(M)$ and its Bases

The module $H(M)$ is implemented as a `DeformedMoebiusAlgebra` over the Laurent polynomial ring $R = \mathbb{Z}[x, x^{-1}]$. It is a free $R$-module with several important bases indexed by the flats $F \in L(M)$.

1.  **Natural Basis ($E$)**:
    *   Basis elements: $\{e_F : F \in L(M)\}$.
    *   This is the standard basis of the Möbius algebra.

2.  **Chow Basis ($C$)**:
    *   A basis that incorporates the Chow polynomials of minors.
    *   Transformation: $C_F = \sum_{G \leq F} x^{\text{rk}(F) - \text{rk}(G)} H_{M^F_G}(x^{-2}) e_G$
    *   Here $H_{M^F_G}$ is the Poincaré polynomial (Chow polynomial) of the minor $M|_F / G$.
    *   Let Pal(k) denote all the Laurent polynomials that satisfy $P(x) = x^k P(x^{-1})$. Then $H_{M^F_G} \in Pal(\text{rk}(M^F_G - 1))$.

3.  **Zeta Basis ($Z$)**:
    *   Basis elements: $\{z_F : F \in L(M)\}$.
    *   Transformation: $Z_F = \sum_{G \leq F} x^{\text{rk}(F) - \text{rk}(G)} P_{M^F_G}(x^{-2}) e_G$
    *   where $P$ is the Kazhdan-Lusztig polynomial.

4.  **Inverse-F Basis ($invF$)**:
    *   Transformation involves the right augmented Chow function $F = H \cdot f^{\text{rev}}$ and the Möbius function:
    *   $invF_F = \sum_{G \leq F} x^{\text{rk}(F) - \text{rk}(G)} (\mu^{\text{rev}} \cdot F)(M^F_G)(x^{-2}) e_G$

### Perverse Subgroups and Modules

The incidence algebra structure allows for the definition of special subgroups of $\mathcal{H}(M)$ based on palindromicity. Let $\text{Pal}(n)$ be the set of Laurent polynomials $f$ such that $f(x) = x^n f(x^{-1})$.

1.  **Perverse Subgroup $\mathcal{H}_p(M)$**:
    *   Consists of elements $\alpha = \sum \alpha_F e_F$ where:
        1. $\alpha_F \in \mathbb{Z}[x]$ (polynomial coefficients).
        2. $S_F(\alpha) \in \text{Pal}(0)$ for all flats $F$.
    *   The Kazhdan-Lusztig basis $\{z_F\}$ forms a $\mathbb{Z}$-basis for $\mathcal{H}_p(M)$.

2.  **The Module $S(M)$** (formerly denoted $\mathcal{H}'_p(M)$):
    *   Consists of all elements $\alpha \in \mathcal{H}(M)$ such that $S_F(\alpha) \in \text{Pal}(0)$ for all $F$.
    *   This is a $\text{Pal}(0)$-module.
    *   The Chow basis $\{c_F\}$ forms a $\text{Pal}(0)$-basis for $S(M)$.
    *   Key property: For any $\alpha \in S(M)$, the coefficient $q_F$ in the Chow expansion $\alpha = \sum q_F c_F$ is the unique $\text{Pal}(0)$ component of the standard coefficient $\alpha_F$.

### Maps on the Module

1.  **The Map $T_H: \mathcal{H}(M) \to R$**:
    *   Defined effectively to select components: $T_H(c^F) = \delta_{H, F}$ and $T_H(e^F) = \delta_{H, F}$.
    *   It acts on polynomials by extracting their $\text{Pal}(0)$ part.
    *   The map is not $R$-linear but is $\text{Pal}(0)$-linear.

2.  **Symmetry Operation $S_H$**:
    *   Defined as $S_F(\alpha) := \sum_{G \ge F} x^{\text{rk}(F)-\text{rk}(G)} \alpha_G$.
    *   The map $S_H: F \mapsto x^{\text{rk}(H) - \text{rk}(F)}$ extends to an involution on the module related to the palindromicity of the basis coefficients?


## Other bases

1.  The basis {$b^F$} is defined as:
    $$b^F = \sum_{G \ge F} x^{\text{rk}(G) - \text{rk}(F)} (\mu^\text{rev} \cdot F)_{M^F_G}(x^{-2}) e_G.$$

    *   It satisfies the following properties:
        *   $b^F \in S(M)$ for all $F \in L(M)$.
        *   $b^F$ form a $\text{Pal}(0)$-basis for $S(M)$.

2.  The basis {$\mu^F$} is defined as:
    $$\mu^F = \sum_{G \ge F} x^{\text{rk}(G) - \text{rk}(F)} \mu_{M^F_G}(x^{-2}) \cdot e_G$$
    where $\mu$ is the Möbius function of the lattice of flats.

    *   It satisfies the following properties:
        *   $\mu^F \in S(M)$ for all $F \in L(M)$.
        *   $\mu^F$ form a $\text{Pal}(0)$-basis for $S(M)$.
        *   $\mu^F$ is the dual of $S_F$ with respect to the inner product $\langle S_H, \mu^F \rangle = S_H(\mu^F) = \delta_{H, F}$.

    *   If $\alpha = \sum \alpha_F e_F \in H(M)$, then $\alpha = \sum \langle S_F, \alpha \rangle \mu^F$. This allows for a quick way to check if an element is in $S(M)$.

## Symmetry Properties

The right augmented Chow function satisfies:
$$F_{st}(x) = x^{\rho_{st}} F_{st}(x^{-1})$$
where $\rho_{st} = \text{rk}(t) - \text{rk}(s)$. For the whole matroid, it's palindromic with respect to the rank.
