"""
Closed-Form Bootstrapping for Projective Geometry Matroids PG(r-1, q)

This module implements the closed-form polynomial computation for standard Chow polynomials H_r(x) 
and Right Augmented Chow polynomials F_r(x) of projective geometry matroids PG(r-1, q).

Mathematical Context:
1. Every flat F of rank k in PG(r-1, q) is modular, so P_{PG(r-1, q)/F}(x) = 1.
2. The reversed KL polynomial is P^{rev}_{PG(r-1, q)/F}(x) = x^{r-k}.
3. The convolution identity holds:
      F_r(x) = sum_{k=0}^r [r choose k]_q * x^{r-k} * H_k(x)
4. By enforcing the palindromic symmetry on F_r(x) (and H_r(x)), the coefficients of H_r(x) 
   and F_r(x) are uniquely determined recursively without having to construct the lattice of flats!
"""

import sys
import os
import sympy as sp

def q_binomial(n, k, q=2):
    """
    Computes the q-binomial (Gaussian) coefficient [n choose k]_q.
    This equals the number of k-dimensional subspaces of an n-dimensional vector space over GF(q).
    """
    if k < 0 or k > n:
        return 0
    num, den = 1, 1
    for i in range(k):
        num *= (q**(n - i) - 1)
        den *= (q**(k - i) - 1)
    return num // den

def compute_projective_polynomials(max_rank, q=2):
    """
    Computes the right augmented Chow polynomial F_r(x) and standard Chow polynomial H_r(x)
    for PG(r-1, q) up to rank `max_rank` by bootstrapping the palindromic constraint.
    
    Returns:
        F (dict): {r: sp.Poly} mapping rank r to Right Augmented Chow polynomial F_r(x)
        H (dict): {r: sp.Poly} mapping rank r to standard Chow polynomial H_r(x)
    """
    x = sp.Symbol('x')
    H = {}
    F = {}
    
    # Base cases for rank 0
    H[0] = sp.poly(1, x)
    F[0] = sp.poly(1, x)
    
    for r in range(1, max_rank + 1):
        # 1. Compute the partial F_r without the top flat's Chow polynomial H_r
        partial_F = 0
        for k in range(r):
            partial_F += q_binomial(r, k, q=q) * (x**(r - k)) * H[k].as_expr()
        
        partial_F = sp.poly(partial_F, x)
        
        # 2. Set up symbolic coefficients for H_r(x), which has degree r-1
        coeffs = [sp.Symbol(f'c_{i}') for i in range(r)]
        H_r_expr = sum(coeffs[i] * (x**i) for i in range(r))
        
        # 3. Construct the full symbolic F_r(x)
        F_r_expr = partial_F.as_expr() + H_r_expr
        F_r_poly = sp.poly(F_r_expr, x)
        
        F_coeffs = [F_r_poly.coeff_monomial(x**i) for i in range(r + 1)]
        
        # 4. Enforce the palindromic property on F_r(x) and H_r(x)
        equations = []
        for i in range((r + 1) // 2):
            equations.append(sp.Eq(F_coeffs[i], F_coeffs[r - i]))
            
        for i in range(r // 2):
            equations.append(sp.Eq(coeffs[i], coeffs[r - 1 - i]))
            
        # 5. Solve the determined linear system for the coefficients of H_r
        sol = sp.solve(equations, coeffs)
        
        H_r_solved = sum(sol[coeffs[i]] * (x**i) for i in range(r))
        H[r] = sp.poly(H_r_solved, x)
        F[r] = sp.poly(partial_F.as_expr() + H_r_solved, x)
        
    return F, H

def print_projective_polynomials(max_rank, q=2):
    """
    Utility function to display the computed polynomials F_r(x) and H_r(x).
    """
    F, H = compute_projective_polynomials(max_rank, q=q)
    print(f"==================================================")
    print(f" Closed-Form Polynomials for PG(r-1, {q})")
    print(f"==================================================\n")
    for r in range(1, max_rank + 1):
        print(f"Rank {r} (PG({r-1}, {q})):")
        print(f"  F_{r}(x) = {F[r].as_expr()}")
        print(f"  H_{r}(x) = {H[r].as_expr()}\n")

if __name__ == "__main__":
    max_r = 6
    if len(sys.argv) > 1:
        max_r = int(sys.argv[1])
    q_val = 2
    if len(sys.argv) > 2:
        q_val = int(sys.argv[2])
    print_projective_polynomials(max_r, q=q_val)
