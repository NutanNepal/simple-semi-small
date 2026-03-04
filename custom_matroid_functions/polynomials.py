"""
Polynomial functions for matroids.

This module contains custom implementations of various polynomial computations
for matroids, including characteristic polynomials, Kazhdan-Lusztig polynomials,
and Q-polynomials.
"""

from sage.all import *
from .core import characteristic_polynomial
import json
import os

# Global polynomial ring
R = PolynomialRing(QQ, 't')
S = PolynomialRing(ZZ, 't')
t = R.gen()

KL_POLY_CACHE_FILE = "kl_polynomial_cache.json"
KL_INV_POLY_CACHE_FILE = "kl_inverse_polynomial_cache.json"

def _load_cache(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                cache_data = json.load(f)
                cache = {}
                for matroid_repr, poly_str in cache_data.items():
                    cache[matroid_repr] = S(poly_str)
                return cache
        except Exception as e:
            print(f"Warning: Could not load cache file {filename}: {e}")
            return {}
    return {}

def _save_cache(cache, filename):
    cache_data = {k: str(v) for k, v in cache.items()}
    try:
        with open(filename, 'w') as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save cache file {filename}: {e}")

def _get_matroid_key(M):
    rank = M.rank()
    size = len(M.groundset())
    try:
        can = M.canonical_form()
        return f"matroid_{rank}_{size}_{str(can)}"
    except AttributeError:
        bases = tuple(sorted(tuple(sorted(b)) for b in M.bases()))
        return f"matroid_{rank}_{size}_{str(bases)}"

# KL polynomial cache
_kl_poly_cache = _load_cache(KL_POLY_CACHE_FILE)
_kl_inv_poly_cache = _load_cache(KL_INV_POLY_CACHE_FILE)

def get_kl_polynomial(M):
    global _kl_poly_cache
    matroid_key = _get_matroid_key(M)
    if matroid_key in _kl_poly_cache:
        return _kl_poly_cache[matroid_key]
    # Compute the polynomial
    if hasattr(M, 'is_uniform') and M.is_uniform():
        r, n = M.rank(), M.size()
        poly = kazhdan_lustig_uniform(r, n)
    else:
        R = LaurentPolynomialRing(ZZ, 't')
        t = R.gen()
        poly = M.lattice_of_flats().kazhdan_lusztig_polynomial()(t)
    _kl_poly_cache[matroid_key] = poly
    _save_cache(_kl_poly_cache, KL_POLY_CACHE_FILE)
    return poly

def get_kl_inverse_polynomial(M):
    global _kl_inv_poly_cache
    matroid_key = _get_matroid_key(M)
    if matroid_key in _kl_inv_poly_cache:
        return _kl_inv_poly_cache[matroid_key]
    poly = inverse_kazhdan_lustig_polynomial(M)
    _kl_inv_poly_cache[matroid_key] = poly
    _save_cache(_kl_inv_poly_cache, KL_INV_POLY_CACHE_FILE)
    return poly

def clear_kl_polynomial_cache():
    global _kl_poly_cache
    _kl_poly_cache = {}
    if os.path.exists(KL_POLY_CACHE_FILE):
        os.remove(KL_POLY_CACHE_FILE)

def clear_kl_inverse_polynomial_cache():
    global _kl_inv_poly_cache
    _kl_inv_poly_cache = {}
    if os.path.exists(KL_INV_POLY_CACHE_FILE):
        os.remove(KL_INV_POLY_CACHE_FILE)

def save_kl_polynomial_cache():
    _save_cache(_kl_poly_cache, KL_POLY_CACHE_FILE)

def save_kl_inverse_polynomial_cache():
    _save_cache(_kl_inv_poly_cache, KL_INV_POLY_CACHE_FILE)

def get_kl_polynomial_cache_info():
    cache_size = len(_kl_poly_cache)
    return {
        'cache_size': cache_size,
        'cache_file': KL_POLY_CACHE_FILE,
        'file_exists': os.path.exists(KL_POLY_CACHE_FILE),
        'sample_keys': list(_kl_poly_cache.keys())[:5] if _kl_poly_cache else []
    }

def get_kl_inverse_polynomial_cache_info():
    cache_size = len(_kl_inv_poly_cache)
    return {
        'cache_size': cache_size,
        'cache_file': KL_INV_POLY_CACHE_FILE,
        'file_exists': os.path.exists(KL_INV_POLY_CACHE_FILE),
        'sample_keys': list(_kl_inv_poly_cache.keys())[:5] if _kl_inv_poly_cache else []
    }

def export_kl_polynomial_cache_to_csv(filename="kl_polynomials_database.csv"):
    import csv
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Matroid_Key', 'KL_Polynomial'])
        for key, poly in _kl_poly_cache.items():
            writer.writerow([key, str(poly)])

def export_kl_inverse_polynomial_cache_to_csv(filename="kl_inverse_polynomials_database.csv"):
    import csv
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Matroid_Key', 'KL_Inverse_Polynomial'])
        for key, poly in _kl_inv_poly_cache.items():
            writer.writerow([key, str(poly)])

def inverse_kazhdan_lustig_uniform(r, n):
    """
    Compute the inverse Kazhdan-Lusztig polynomial for uniform matroid U(r,n).
    INPUT:
    - r: rank of the uniform matroid
    - n: size of the groundset
    OUTPUT:
    - Inverse Kazhdan-Lusztig polynomial as a polynomial in t (integer coefficients)
    """
    m, d = n-r, r
    upper_bound = (d-1)//2
    sum = R(0)
    for j in range (0, upper_bound + 1):
        coeff = binomial(m+d, d) * m * (d - 2 * j)/((m + j) * (m + d - j)) * (binomial(d, j))
        sum = sum + coeff * t**(j)
    return S(sum)

def kazhdan_lustig_uniform(r, n):
    """
    Compute the Kazhdan-Lusztig polynomial for uniform matroid U(r,n).
    INPUT:
    - r: rank of the uniform matroid
    - n: size of the groundset
    OUTPUT:
    - Kazhdan-Lusztig polynomial as a polynomial in t (integer coefficients)
    """
    m, d = n - r, r
    upper_bound = (d-1)//2
    sum = R(0)
    for i in range(0, upper_bound + 1):
        s = R(0)
        for h in range(0, m):
            s = s + binomial(d - i + h, h + i + 1) * binomial(i - 1 + h, h)
        s = s * binomial(m + d, i)/(d - i)
        sum = sum + s * t**(i)
    return S(sum)

def q_kl(k, h):
    """
    Helper function for KL inverse computations.
    
    INPUT:
    - k: rank parameter
    - h: height parameter
    
    OUTPUT:
    - Difference of inverse KL polynomials
    """
    return inverse_kazhdan_lustig_uniform(k, h+1) - inverse_kazhdan_lustig_uniform(k-1, h)

def inverse_kazhdan_lustig_polynomial(M):
    """
    Compute inverse Kazhdan-Lusztig polynomial for a matroid.
    
    This is a fast implementation that works for uniform matroids
    and some other special cases.
    
    INPUT:
    - M: a matroid
    
    OUTPUT:
    - Inverse KL polynomial as a polynomial in t with integer coefficients
    """
    if M.loops(): 
        return S(0)
    k, n = M.rank(), M.size()
    if k == n or k == 0: 
        return S(1)
    if not M.is_connected():
        ans = S(1)
        CC = M.components()
        for N in CC:
            res = M.delete(M.groundset() - N)
            ans = ans * inverse_kazhdan_lustig_polynomial(res)
        return S(ans)

    from .extensions import is_paving
    if is_paving(M):
        return kl_inverse_paving(M)
    if is_paving(M.dual()):
        return kl_inverse_copaving(M)
    
    LF = M.lattice_of_flats()
    ans = R(0)
    for F in LF:
        if len(F) != n:
            Res = M.delete(M.groundset() - F)
            Con = M.contract(F)
            chi = characteristic_polynomial(Con)(1/t) * t**(Con.rank())
            PPP = inverse_kazhdan_lustig_polynomial(Res)(t) * (-1)**(Res.rank())
            ans = ans + chi * PPP
    assert (t**k * ans(1/t)).numerator() == -ans(t)
    ans = ans.numerator() * (-1)**(k+1)
    result = ans.truncate((k+1)//2)
    return S(result)

# Alias for backward compatibility and convenience
invkl = inverse_kazhdan_lustig_polynomial

def kl_inverse_paving(M):
    """
    Compute inverse KL polynomial for paving matroids.
    
    INPUT:
    - M: a paving matroid
    
    OUTPUT:
    - Inverse Kazhdan-Lusztig polynomial
    """
    from .extensions import is_paving
    assert is_paving(M)
    n = M.size()
    k = M.rank()
    ans = inverse_kazhdan_lustig_uniform(k, n)
    for H in M.hyperplanes():
        h = len(H)
        if h >= k:
            ans = ans - q_kl(k, h)
    return S(ans)

def kl_inverse_copaving(M):
    """
    Compute inverse KL polynomial for copaving matroids.
    
    INPUT:
    - M: a copaving matroid
    
    OUTPUT:
    - Inverse Kazhdan-Lusztig polynomial
    """
    from .extensions import is_paving
    assert is_paving(M.dual())
    n = M.size()
    k = M.rank()
    ans = inverse_kazhdan_lustig_uniform(k, n)
    for H in M.dual().hyperplanes():
        h = len(H)
        if h >= n-k:
            ans = ans - kli_vtilde_dual(n-k, h, n) + inverse_kazhdan_lustig_uniform(h-n+k+1, h) * inverse_kazhdan_lustig_uniform(n-h-1, n-h)
    return S(ans)

def kli_vtilde_dual(k, h, n):
    """
    Helper function for dual KL inverse computations.
    """
    return helper1(n-k, h, n)

def helper1(k, h, n):
    """
    Helper function for KL inverse computations.
    """
    c = n - h
    ans1 = inverse_kazhdan_lustig_uniform(k, n)
    ans2 = helper2(c, k, n)
    ans3 = inverse_kazhdan_lustig_uniform(k-c+1, h) * inverse_kazhdan_lustig_uniform(c-1, c)
    return ans1 - ans2 + ans3

def helper2(c, k, n):
    """
    Helper function for KL inverse computations.
    """
    h = n - c
    ans = 0
    for j in range(k-c+1):
        ans = ans + binomial(n-c, j) * (-1)**(c-1+j) * inverse_kazhdan_lustig_uniform(c-1, c) * t**(k-c-j+1) * chuly(k-c-j+1, n-c-j)(1/t)
    for i in range(c-1):
        for j in range(k-i):
            ans = ans + binomial(c, i) * binomial(n-c, j) * (-1)**(i+j) * t**(k-i-j) * helper4(c, k, n, i, j)(1/t)
    ans = ans.numerator().truncate((k-1)//2 + 1)
    if ans[0] < 0:
        ans = -ans
    return ans

def helper3(c, k, n):
    """
    Helper function for KL inverse computations.
    """
    ans = 0
    for j in range(k-c+1):
        ans = ans + binomial(n-c, j) * kazhdan_lustig_uniform(c-1, c) * (-1)**(k-c-j+1) * inverse_kazhdan_lustig_uniform(k-c-j+1, n-c-j)
    for i in range(c-1):
        for j in range(k-i):
            ans = ans + binomial(c, i) * binomial(n-c, j) * (-1)**(k-i-j) * helper2(c-i, k-i-j, n-i-j)
    return -ans

def helper4(c, k, n, i, j):
    """
    Helper function for KL inverse computations.
    """
    ans = 0
    for l in range(c-i-1):
        ans = ans + (-1)**l * (t-1)**(max(n-i-j-l-1, 0))
    for u in range(n-k-1):
        ans = doit_once(ans)
    return ans

def chuly(a, b):
    """
    Helper function for KL inverse computations.
    """
    ans = (t-1)**b
    for i in range(b-a):
        ans = doit_once(ans)
    return ans

def doit_once(p):
    """
    Helper function for KL inverse computations.
    """
    p = p // t**2
    p = p * t
    p = p - p(1)
    return p

def lorenzo(k, h, n):
    """
    Helper function for KL inverse computations.
    """
    c = n - h
    ans1 = kazhdan_lustig_uniform(k, n) + kazhdan_lustig_uniform(k-c+1, h) * kazhdan_lustig_uniform(c-1, c)
    ans2 = helper3(c, k, n)
    return ans1 - ans2

# --- Global Cache for Polynomials ---
global_poly_cache = {}

def get_cache_key(func_name, M):
    return (func_name, tuple(sorted(M.lattice_of_flats())))

def convolve(f, g):
    from sage.rings.polynomial.laurent_polynomial_ring import LaurentPolynomialRing
    from sage.rings.integer_ring import ZZ
    x = LaurentPolynomialRing(ZZ, 'x').gen()
    
    def memoized_conv(M):
        # f and g are functions. We can't easily hash them, so we just run them
        # Note: convolve itself returns a function. We'll cache the result
        # based on id of f and g to distinguish
        key = ("convolve", id(f), id(g), tuple(sorted(M.lattice_of_flats())))
        if key not in global_poly_cache:
            global_poly_cache[key] = sum(f(M.delete(M.groundset() - F))(x) * g(M.contract(F))(x) for F in list(M.lattice_of_flats()))
        return global_poly_cache[key]
    return memoized_conv

def rev(f):
    from sage.rings.polynomial.laurent_polynomial_ring import LaurentPolynomialRing
    from sage.rings.integer_ring import ZZ
    LPoly = LaurentPolynomialRing(ZZ, 'x')
    x = LPoly.gen()
    
    def memoized_rev(M):
        # Use a more robust key than id(f) if f is a local lambda
        key = ("rev", f.__name__ if hasattr(f, '__name__') else id(f), tuple(sorted(M.lattice_of_flats())))
        
        if key not in global_poly_cache:
            poly = f(M)
            # Use substitution instead of __call__ to be explicit
            # This avoids issues if 'x' is shadowed in this scope
            rev_poly = poly.subs({poly.parent().gen(): x**-1}) * x**M.rank()
            global_poly_cache[key] = rev_poly
            
        return global_poly_cache[key]
    return memoized_rev

def kl_poly(M):
    return get_kl_polynomial(M)

def mu(M):
    from .core import characteristic_polynomial
    key = ("mu", tuple(sorted(M.lattice_of_flats())))
    if key not in global_poly_cache:
        global_poly_cache[key] = characteristic_polynomial(M)(0)
    return global_poly_cache[key]