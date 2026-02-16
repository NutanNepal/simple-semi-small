"""
Series method for Chow polynomial recurrence (experimental).

Builds generating functions:
  H_K(z) = sum_{i>=1} H_Ki * z^i / i!
  D(z)   = exp((1+x) * H_K(z))

The exponential D(z) encodes the "add a component" structure. The recurrence
  H_{K_{n+1}} = (1-ny)H_{K_n} + y * sum_{lambda} C_lambda * |lambda| * H_{K_{|lambda|}} * H_oplus(lambda)
can be related to D'(z) = (1+x) * D(z) * H_K'(z) under suitable interpretation.

For now, this module provides the series construction for validation.
Use the integer partition loop in complete_graph_recurrence_integer_partitions.ipynb
for actual computation.
"""

from sage.all import factorial, LaurentPolynomialRing, QQ


def fast_RHS_series_method(n, P, x, _Kn_cache):
    """
    Construct the series H_K(z) and D(z) = exp((1+x)*H_K(z)) up to order n.

    INPUT:
    - n: int, max order
    - P: LaurentPolynomialRing(QQ, 'x')
    - x: generator of P
    - _Kn_cache: dict {i: H_Ki} for i=1..n (from compute_sequence)

    OUTPUT:
    - H_K_series: power series in z with coefficients in P
    - D_series: exp((1+x)*H_K_series)
    """
    # Power series ring: R = P[[z]], coefficients are Laurent polynomials in x
    R = P[['z']]
    z = R.gen()

    # H_K(z) = sum_{i=1..n} H_Ki * z^i / i!
    H_K_series = R(0)
    for i in range(1, n + 1):
        if i in _Kn_cache:
            H_K_series += _Kn_cache[i] * z**i / factorial(i)

    # D(z) = exp((1+x) * H_K(z))
    D_series = ((1 + x) * H_K_series).exp()

    return H_K_series, D_series


def validate_series(n, P, x, _Kn_cache):
    """
    Validate the series construction: check that H_K_series has correct
    coefficients and D_series is well-defined.
    """
    H_K_series, D_series = fast_RHS_series_method(n, P, x, _Kn_cache)

    # Check H_K_series coefficients match _Kn_cache
    for i in range(1, n + 1):
        if i in _Kn_cache:
            coef = H_K_series[i]
            expected = _Kn_cache[i] / factorial(i)
            if coef != expected:
                return False, f"H_K_series[{i}] mismatch: got {coef}, expected {expected}"

    # D(0) = exp(0) = 1
    if D_series[0] != P(1):
        return False, f"D(0) = {D_series[0]}, expected 1"

    return True, (H_K_series, D_series)


# --- Example usage (run from notebook after compute_sequence) ---
# from fast_RHS_series import fast_RHS_series_method, validate_series
# H_K_ser, D_ser = fast_RHS_series_method(6, P, x, _Kn_cache)
# ok, result = validate_series(6, P, x, _Kn_cache)
