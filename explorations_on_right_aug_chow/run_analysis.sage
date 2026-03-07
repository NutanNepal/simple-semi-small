import sys
import os

# Setup paths
current_dir = os.getcwd() # Should be project root if run from there
sys.path.insert(0, current_dir)

from sage.all import *
from custom_matroid_functions import chow_polynomial, kl_poly, convolve, rev

P = LaurentPolynomialRing(ZZ, 'x')
x = P.gen()

def chow_poly_fn(M):
    return P(chow_polynomial(M))

def kl_rev_fn(M):
    p = kl_poly(M)
    # Note: kl_poly returns a polynomial in t
    t = p.parent().gen()
    rk = M.rank()
    return P(p.subs({t: x**-1}) * x**rk)

def get_matroid_key(M):
    rank = M.rank()
    size = len(M.groundset())
    try:
        can = M.canonical_form()
        return (rank, size, str(can))
    except AttributeError:
        bases = tuple(sorted(tuple(sorted(b)) for b in M.bases()))
        return (rank, size, str(bases))

_inv_cache_global = {}

def convolution_inverse(f, name):
    cache_inv = {}
    
    def f_inv(M):
        m_key = (name, get_matroid_key(M))
        if m_key in _inv_cache_global:
            return _inv_cache_global[m_key]
        
        if M.rank() == 0 and M.size() == 0:
            res = 1 / f(M)
            _inv_cache_global[m_key] = res
            return res
        
        # Identity is epsilon: (f * f_inv)(M) = 0 for non-empty M
        # sum_{F} f(M|F) f_inv(M/F) = 0
        # f(M|empty) f_inv(M/empty) + sum_{F != empty} f(M|F) f_inv(M/F) = 0
        # f(empty) f_inv(M) = - sum_{F != empty} f(M|F) f_inv(M/F)
        
        empty_matroid = matroids.Uniform(0, 0)
        f0 = f(empty_matroid)
        
        L = M.lattice_of_flats()
        E = M.groundset()
        
        total = P(0)
        for F in L:
            if len(F) == 0: continue
            restriction = M.delete(list(set(E) - set(F)))
            contraction = M.contract(list(F))
            total += f(restriction) * f_inv(contraction)
            
        res = -total / f0
        _inv_cache_global[m_key] = res
        return res
    
    return f_inv

# G = kl_rev * chow
G_fn = convolve(kl_rev_fn, chow_poly_fn)
# F = chow * kl_rev
F_fn = convolve(chow_poly_fn, kl_rev_fn)

G_inv_fn = convolution_inverse(G_fn, "G")
F_inv_fn = convolution_inverse(F_fn, "F")

def analyze_matroid(M, label):
    print(f"\n--- Analysis for {label} ({M}) ---")
    f_val = F_fn(M)
    g_val = G_fn(M)
    print(f"F(M): {f_val}")
    print(f"G(M): {g_val}")
    
    # Compute G^-1 * F (M)
    # (G^-1 * F)(M) = sum_{F} G^-1(M|F) F(M/F)
    L = M.lattice_of_flats()
    E = M.groundset()
    
    g_inv_star_f = P(0)
    for F in L:
        res = M.delete(list(set(E) - set(F)))
        con = M.contract(list(F))
        g_inv_star_f += G_inv_fn(res) * F_fn(con)
    
    print(f"G^-1 * F (M): {g_inv_star_f}")
    
    f_inv_star_g = P(0)
    for F in L:
        res = M.delete(list(set(E) - set(F)))
        con = M.contract(list(F))
        f_inv_star_g += F_inv_fn(res) * G_fn(con)
    
    print(f"F^-1 * G (M): {f_inv_star_g}")

# Test matroids
# Systematic test for Uniform matroids
print("\n=== Systematic Test for Uniform Matroids ===")
for r in range(1, 5):
    for n in range(r, r + 4):
        M = matroids.Uniform(r, n)
        # Compute G^-1 * F (M)
        L = M.lattice_of_flats()
        E = M.groundset()
        res_conv = P(0)
        for F in L:
            res_conv += G_inv_fn(M.delete(list(set(E) - set(F)))) * F_fn(M.contract(list(F)))
        print(f"U({r}, {n}): {res_conv}")
