import sys
import os

# Add project root and the-machine to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "the-machine"))

from sage.all import *
from HM_module import *
from custom_matroid_functions import *

P = LaurentPolynomialRing(ZZ, 'x')
x = P.gen()

def convolve(f, g, M):
    sum = P(0)
    L = M.lattice_of_flats()
    E = M.groundset()
    for F in L:
        m_f = M.delete(E - F)
        m_g = M.contract(F)
        sum += f(m_f)(x) * g(m_g)(x)
    return sum

def chow(M):
    return chow_polynomial(M)

def kl_rev(M):
    p = M.lattice_of_flats().kazhdan_lusztig_polynomial()(x)
    return p(x**-1) * x**M.rank()

def right_aug_chow(M):
    return convolve(chow, kl_rev, M)

def chi(M):
    return characteristic_polynomial(M)(x)

def f_poly(M):
    return M.lattice_of_flats().kazhdan_lusztig_polynomial()(x)

def left_aug_chow_f_chi_h(M):
    # G = (f * chi) * H
    g_rev_func = lambda m: convolve(f_poly, chi, m)
    return convolve(g_rev_func, chow, M)

def left_aug_chow(M):
    return left_aug_chow_f_chi_h(M)

def left_aug_chow_alt1(M):
    # G = H * kl
    return convolve(chow, lambda m: m.lattice_of_flats().kazhdan_lusztig_polynomial()(x), M)

def left_aug_chow_alt2(M):
    # G = Aug(M) = convolve(zeta, H)
    return convolve(lambda m: P(1), chow, M)

def psi_s(s_matroid):
    rk = s_matroid.rank()
    h = chow_polynomial(s_matroid)
    h_rev = h(x**-1) * x**rk
    return x**rk * h_rev(x**-2)

def verify_psi_on_kl_basis(M):
    L = M.lattice_of_flats()
    Eq_M = create_deformed_algebra(M, base_ring=P)
    E_basis = Eq_M.natural().basis()
    Z_basis = Eq_M.zeta().basis()
    
    for t in L:
        kl_t = Z_basis[t]
        e_coeffs = Eq_M.natural()(kl_t).monomial_coefficients()
        
        image_psi = P(0)
        for s, coeff in e_coeffs.items():
            image_psi += coeff * psi_s(M.delete(M.groundset() - s))
        
        m_t = M.delete(M.groundset() - t)
        f_mt = right_aug_chow(m_t)
        target = x**m_t.rank() * f_mt(x**-2)
        
        if image_psi != target:
            print(f"Flat {t} failed!")
            print(f"Image: {image_psi}")
            print(f"Target: {target}")
            return False
    return True

# Test Conjecture F = G
print("Testing F = G variations...")
for n in range(2, 5):
    M = matroids.CompleteGraphic(n)
    F = right_aug_chow(M)
    G = left_aug_chow(M)
    G1 = left_aug_chow_alt1(M)
    G2 = left_aug_chow_alt2(M)
    print(f"K_{n}:")
    print(f"  F: {F}")
    print(f"  G: {G}")
    print(f"  G1: {G1}")
    print(f"  G2: {G2}")

for n in range(2, 5):
    for k in range(1, n):
        M = matroids.Uniform(k, n)
        F = right_aug_chow(M)
        G = left_aug_chow(M)
        if F != G:
            print(f"U_{k,n} Failed: F != G")
            sys.exit(1)
        print(f"U_{k,n} OK")

# Test Map Psi
print("\nTesting Map Psi on KL basis...")
M = matroids.CompleteGraphic(3)
if verify_psi_on_kl_basis(M):
    print("Map Psi OK for K_3")
else:
    sys.exit(1)

M = matroids.catalog.Fano()
if verify_psi_on_kl_basis(M):
    print("Map Psi OK for Fano")
else:
    sys.exit(1)

print("\nAll tests passed!")
