import sys
import os
from sage.all import *

sys.path.append(os.path.abspath('.'))
from custom_matroid_functions.polynomials import inverse_kazhdan_lustig_uniform

print("Searching for a uniform matroid whose inverse KL polynomial is not real-rooted...")

found = False
for n in range(2, 40):
    for r in range(1, n):
        try:
            poly = inverse_kazhdan_lustig_uniform(r, n)
            d = poly.degree()
            if d > 1:
                # To check real rootedness robustly:
                num_real_roots = sum(m for root, m in poly.roots(AA))
                if num_real_roots < d:
                    print(f"Found non-real-rooted example: U({r}, {n})")
                    print(f"Inverse KL Polynomial: {poly}")
                    print(f"Degree: {d}, Number of real roots: {num_real_roots}")
                    print(f"Roots in CC: {poly.roots(CC)}")
                    found = True
                    break
        except Exception as e:
            print(f"Error computing U({r}, {n}): {e}")
    if found:
        break

if not found:
    print("Could not find any non-real-rooted examples up to n=39.")
