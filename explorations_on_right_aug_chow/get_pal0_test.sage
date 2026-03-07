from sage.all import *

P.<x> = LaurentPolynomialRing(ZZ)

def get_pal0_part(f):
    """
    Extracts the Pal(0) part of a Laurent polynomial f.
    Any Laurent polynomial f can be uniquely written as f_0 + f_2
    where f_0 in Pal(0) and f_2 in Pal(2).
    f_0 = (x^2 * f(x^-1) - f(x)) / (x^2 - 1)
    """
    if f == 0:
        return P(0)
    
    # Ensure f is in the Laurent Polynomial Ring
    f = P(f)
    x_var = P.gen()
    
    # Calculate f(x^-1)
    # We substitute x with x^-1
    f_inv = f.subs({x_var: x_var**-1})
    
    numerator = x_var**2 * f_inv - f
    denominator = x_var**2 - 1
    
    # The division should be exact in the fraction field, and the result 
    # should be a Laurent polynomial.
    q, r = numerator.quo_rem(denominator)
    if r != 0:
        raise ValueError(f"Division not exact, remainder: {r}")
    return q

# Test
test_poly = 1 + x + x**2
print("Test poly:", test_poly)
print("Pal(0) part:", get_pal0_part(test_poly))

test_poly2 = 3*x**-1 + 5 + 3*x
print("Test poly2:", test_poly2)
print("Pal(0) part:", get_pal0_part(test_poly2))
