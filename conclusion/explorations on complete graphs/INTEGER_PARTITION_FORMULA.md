# Integer Partition Formula: Validity Check

## Claim

The recurrence can be computed by summing over **integer partitions** $\lambda \vdash n$ instead of set partitions:

$$H_{K_{n+1}}(y) = (1 - ny)\, H_{K_n}(y) + y \sum_{\lambda \vdash n} C_\lambda \cdot |\lambda| \cdot H_{K_{|\lambda|}}(y) \cdot H_{\oplus}(\lambda, y)$$

## Validity

### 1. Invariant depends only on block sizes ✓

The restriction $M|F$ for a flat $F$ is the graphic matroid of the disjoint union of cliques on the blocks of the partition induced by $F$. This matroid is determined up to isomorphism by the **multiset of block sizes** $\{|B_1|, |B_2|, \ldots\}$, not by which vertices lie in which block. So $H_{M|F}$ depends only on the integer partition shape $\lambda$.

### 2. Coefficient $C_\lambda$ ✓

The number of set partitions of $\{1,\ldots,n\}$ with shape $\lambda = (\lambda_1, \ldots, \lambda_k)$ (with $m_j$ parts of size $j$) is:

$$C_\lambda = \frac{n!}{\prod_{j} (j!)^{m_j} \cdot m_j!}$$

**Derivation:** Assign $n$ labeled elements to $k$ unlabeled blocks with prescribed sizes. Multinomial coefficient $n!/(\lambda_1! \cdots \lambda_k!)$ counts assignments when blocks are labeled. Dividing by $\prod_j m_j!$ makes blocks of the same size indistinguishable. Since $\prod_i \lambda_i! = \prod_j (j!)^{m_j}$, the formula follows.

### 3. Direct sum matroid ✓

$H_{\oplus}(\lambda, y)$ is the Chow polynomial of $K_{\lambda_1} \oplus K_{\lambda_2} \oplus \cdots \oplus K_{\lambda_k}$, built as the cycle matroid of the disjoint union of complete graphs. This matches the matroid $M|F$ for any set partition with shape $\lambda$.

### 4. Empirical verification

The notebook `complete_graph_recurrence_integer_partitions.ipynb` verifies that the integer partition method yields the same RHS as the set partition method for small $n$.
