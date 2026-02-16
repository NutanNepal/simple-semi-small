# Algorithm Outline: Chow Polynomial Recurrence for Complete Graphs

This document outlines the algorithms and logic for computing $H_{K_n}(y)$ recursively. It will be updated as the derivation is refined.

---

## Conjectured Recurrence

$$H_{K_{n+1}}(y) = (1 - ny)\, H_{K_n}(y) + \sum_{i = T_n+1}^{T_{n+1}} \sum_{F \in S_i(M^i)} y \cdot H_{n-\operatorname{rk}(F)}(y) \cdot H_{M^F}(y)$$

### Notation (to be refined)

| Symbol | Meaning |
|--------|---------|
| $T_n$ | Triangular number: $T_n = \binom{n}{2} = \frac{n(n-1)}{2}$ = number of edges in $K_n$ |
| $T_{n+1}$ | $= \binom{n+1}{2}$ = number of edges in $K_{n+1}$ |
| $i$ | Index runs from $T_n+1$ to $T_{n+1}$ (the $n$ star edges) |
| $M^i$ | Matroid at step $i$ (intermediate matroid in the deletion sequence) |
| $S_i(M^i)$ | Valid flats at step $i$ (Component Isolation Rule, see §3) |
| $H_{n-\operatorname{rk}(F)}(y)$ | *(Clarify: $H_{K_{n-\operatorname{rk}(F)}}(y)$?)* |
| $M^F$ | Restriction $M|F$: the matroid on the subgraph $F$. Each flat $F$ is a subgraph, so $M^F$ is the graphic matroid of that subgraph. |
| $H_{M^F}(y)$ | Chow polynomial of $M|F$ (the restriction, not contraction) |

---

## Algorithm Structure

### 1. Labelling and edge indexing

**Labelling:** By **vertex addition**: add vertices 2, 3, …, n. When adding vertex $j$, add edges $(1,j), (2,j), \ldots, (j-1,j)$ in that order:
- $(1,2) \to 1$; $(1,3) \to 2$, $(2,3) \to 3$; $(1,4) \to 4$, $(2,4) \to 5$, $(3,4) \to 6$; $(1,5) \to 7$, …
- Star edges (incident to vertex $n+1$ in $K_{n+1}$) have the **highest labels**.
- **Deletion order:** highest labels first.

- $T_n = |E(K_n)| = \binom{n}{2}$
- Base edges (in $K_n$): $1, \ldots, T_n$
- Star edges: $T_n+1, \ldots, T_{n+1}$

### 2. Matroid sequence $M^i$

- $M^{T_{n+1}} = M(K_{n+1})$ (no deletions)
- $M^{T_n+1} = M(K_n)$ (all star edges deleted)
- For $i = T_n+1, \ldots, T_{n+1}$: $M^i$ = matroid after deleting star edges with label $> i$

*(Map this to the `M(n, i)` convention: deletion step vs edge-label indexing.)*

### 3. Valid flats $S_i(M^i)$ — Component Isolation Rule

**$S_i$ is NOT a full lattice of flats**; it is a meet-semilattice (closed under intersection) obtained by filtering $L(K_n)$.

**Formulas:**
- $k_{\text{del}} = T_{n+1} - i$ (number of star edges deleted so far)
- $v_{\text{target}} = n - k_{\text{del}}$ (vertex whose star we are about to delete; deletion order: $n, n-1, \ldots, 1$)
- $V_{\text{active}} = \{1, 2, \ldots, v_{\text{target}}-1\}$ (vertices that still have star edges)

$$F \in S_i \iff C_{v_{\text{target}}}(F) \cap V_{\text{active}} = \emptyset$$

where $C_v(F)$ is the connected component of the subgraph (flat) $F$ that contains vertex $v$.

**Implementation:** Use Union-Find on the subgraph induced by $F$; reject $F$ if any vertex in $V_{\text{active}}$ lies in the same component as $v_{\text{target}}$. Results are cached in `s_i_cache.json`.

**Restriction:** $M^F = M|F$ is the same whether we restrict $M(K_n)$ or $M^i$ to $F$ (since $F \subseteq E(K_n)$), so we use $M(K_n)$ for all restrictions.

### 4. Lattice sum term

For each $i$ and each $F \in S_i(M^i)$:

$$\text{term} = y \cdot H_{n-\operatorname{rk}(F)}(y) \cdot H_{M^F}(y)$$

Here $M^F = M|F$ is the **restriction** (not contraction): each flat $F$ is a subgraph, so $M^F$ is the matroid on that subgraph.

### 5. Base term

$$(1 - ny)\, H_{K_n}(y)$$

---

## Implementation Checklist

- [ ] Resolve indexing: edge labels vs deletion-step index
- [x] Define $S_i(M^i)$ precisely: Component Isolation Rule (filter $L(K_n)$ by connectivity)
- [x] Cache $S_i$ in `s_i_cache.json`; use $M(K_n)$ for restriction (same as $M^i|F$ when $F \in L(K_n)$)
- [ ] Clarify $H_{n-\operatorname{rk}(F)}$
- [ ] Implement lattice iteration over $S_i(M^i)$
- [ ] Handle degenerate cases (empty set, atoms) per `ab.cursorrules` §3–4
- [ ] Verify parity (no $\sqrt{y}$ terms)

---

## References

- `ab.cursorrules` — derivation summary and corrections
- `complete_graph_recurrence.ipynb` — implementation
