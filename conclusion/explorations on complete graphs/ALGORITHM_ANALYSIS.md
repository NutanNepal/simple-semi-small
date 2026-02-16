# Algorithm Analysis: Chow Polynomial Recurrence for Complete Graphs

Analysis of the two implementations for computing the RHS of
$$H_{K_{n+1}}(y) = (1 - ny)\, H_{K_n}(y) + y \sum_{\text{terms}} H_{n-\operatorname{rk}(F)}(y) \cdot H_{M^F}(y).$$

---

## 1. Problem Parameters

| Symbol | Meaning | Asymptotic |
|--------|---------|------------|
| $n$ | Number of vertices in base graph $K_n$ | Input size |
| $T_n = \binom{n}{2}$ | Edges in $K_n$ | $\Theta(n^2)$ |
| $B_n$ | Bell number = partitions of $\{1,\ldots,n\}$ | $\sim n^{n/\ln n}$ (super-exponential) |
| $L(K_n)$ | Lattice of flats of $M(K_n)$ | $|L(K_n)| = B_n$ |

**Key fact:** Flats of $M(K_n)$ biject with set partitions of $\{1,\ldots,n\}$ (each flat = edge set of disjoint union of cliques).

---

## 2. Flat-Based Algorithm (`complete_graph_recurrence.ipynb`)

### Structure

```
recurrence_RHS(n):
  for i = T_n+1 to T_{n+1}:           # n iterations
    for F in valid_flats_S_i(n, i):   # |S_i| flats per i
      term = x * H_{n-rk(F)} * H_{M|F}
      lattice_sum += term
```

### `valid_flats_S_i(n, i)` (uncached)

1. **Enumerate** all flats: `M_Kn.lattice_of_flats()` → $B_n$ flats
2. **Filter** by Component Isolation Rule: Union-Find on each flat
3. **Return** filtered list

**Per flat:** Union-Find on $\leq T_n$ edges, $O(T_n \cdot \alpha(n)) \approx O(n^2)$.

### Complexity (uncached)

| Step | Cost |
|------|------|
| Outer loop | $n$ iterations |
| Flats per $i$ | $\sum_i |S_i| = \sum_{\pi \in \Pi_n} |\pi|$ (each partition appears $|\pi|$ times) |
| Total lattice terms | $\sum_{\pi} |\pi| = \sum_{k=1}^n k \cdot S(n,k)$ (Stirling II) |
| Filter cost per $i$ | $O(B_n \cdot n^2)$ to scan and test all flats |
| **Total filter** | $O(n \cdot B_n \cdot n^2) = O(n^3 B_n)$ |
| **Chow per term** | Dominant: $H_{M|F}$ and $H_{K_{|\pi|}}$ (see §4) |

### With cache

- **First run:** Compute and cache $S_i$ for each $i$; filter cost $O(n \cdot B_n \cdot n^2)$ once.
- **Subsequent runs:** Load $S_i$ from JSON; filter cost eliminated.
- **Cache size:** $O(\sum_i |S_i|) = O(\sum_{\pi} |\pi|)$ flat representations.

---

## 3. Partition-Based Algorithm (`complete_graph_recurrence_partitions.ipynb`)

### Structure

```
recurrence_RHS_partitions(n):
  for pi in SetPartitions(n):         # B_n iterations
    F = partition_to_flat(pi, ...)   # O(T_n)
    k = |pi|
    term = x * k * H_{K_k} * H_{M|F}
    lattice_sum += term
```

### `partition_to_flat(pi, label_to_edge, n)`

- Build vertex→block map: $O(n)$
- Scan $T_n$ edges: $O(n^2)$
- **Total:** $O(n^2)$ per partition

### Complexity

| Step | Cost |
|------|------|
| Iterations | $B_n$ |
| `partition_to_flat` per partition | $O(n^2)$ |
| **Total overhead** | $O(B_n \cdot n^2)$ |
| **Chow per term** | Same as flat-based (see §4) |

---

## 4. Dominant Cost: Chow Polynomial

Both algorithms compute the same set of Chow polynomials:
- $H_{K_n}$, $H_{K_{n-1}}$, …, $H_{K_1}$ (base terms)
- $H_{M|F}$ for each flat $F$ (restriction to disjoint union of cliques)

### Chow polynomial recursion

```python
chow_polynomial(M):
  for rank r = 1 to rank(M):
    for flat F in M.flats(r):
      restriction_poly = reduced_char(M|F)
      contraction_poly = chow_polynomial(M/F)   # recursive
      chow += restriction_poly * contraction_poly
```

- **Flats per matroid:** For $M(K_m)$, $|L(K_m)| = B_m$.
- **Recursion depth:** $\leq \operatorname{rank}(M)$.
- **Work per node:** Iterate over all flats; each step does restriction, contraction, and recursive Chow.

**Rough complexity:** Exponential in matroid size; dominated by the number of flats and recursion. Caching (`get_chow_polynomial`) avoids recomputation of the same matroid.

---

## 5. Comparison

| Aspect | Flat-based | Partition-based |
|--------|------------|-----------------|
| **Iteration count** | $\sum_i |S_i| = \sum_\pi |\pi|$ (each partition counted $|\pi|$ times) | $B_n$ (each partition once) |
| **Filter/enumeration** | Enumerate $B_n$ flats, filter by Union-Find | Enumerate $B_n$ partitions, map to flat |
| **Filter cost (no cache)** | $O(n^3 B_n)$ | N/A (no filter) |
| **Per-term overhead** | $O(n^2)$ Union-Find (if uncached) | $O(n^2)$ `partition_to_flat` |
| **Cache** | Caches $S_i$ by edge index $i$ | No $S_i$ cache (iterates partitions directly) |
| **Memory** | Needs $s_i$ cache file | No extra cache for structure |

### When flat-based is better

- **With warm cache:** Filter cost is gone; both do the same Chow work.
- **Repeated runs:** Cache makes flat-based faster after the first run.

### When partition-based is better

- **Cold start:** No filter step; avoids $O(n \cdot B_n \cdot n^2)$ Union-Find work.
- **Clarity:** Direct iteration over partitions; no cache management.
- **Memory:** No $S_i$ cache file.

---

## 6. Asymptotic Summary

Let $C(n)$ = cost of computing all Chow polynomials that appear in the recurrence (with caching).

| Algorithm | Dominant cost |
|-----------|----------------|
| Flat-based (cached) | $C(n) + O(B_n)$ (load cache, iterate terms) |
| Flat-based (uncached) | $C(n) + O(n^3 B_n)$ (filter) |
| Partition-based | $C(n) + O(B_n \cdot n^2)$ (partition→flat) |

**Bottleneck:** $C(n)$ (Chow computation) dominates for moderate $n$; both methods have similar iteration structure and benefit from Chow caching.

---

## 7. Recommendations

1. **Use Chow cache** (`get_chow_polynomial`): Critical for both methods.
2. **Partition-based for cold runs:** Simpler and avoids filter cost.
3. **Flat-based for repeated $n$:** Use when $S_i$ cache is warm.
4. **Scaling:** $B_n$ grows super-exponentially; expect $n \geq 10$ to be slow without aggressive caching.
