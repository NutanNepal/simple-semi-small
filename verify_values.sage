import sys
import os

sys.path.insert(0, os.path.abspath('.'))
from custom_matroid_functions import *
from sage.all import *

def verify():
    print(f"H(K_4) = {get_chow_polynomial(matroids.CompleteGraphic(4))}")
    print(f"H(W_3) = {get_chow_polynomial(matroids.catalog.Wheel(3))}")
    print(f"H(K_3) = {get_chow_polynomial(matroids.CompleteGraphic(3))}")
    print(f"H(U(3,4)) = {get_chow_polynomial(matroids.Uniform(3, 4))}")

if __name__ == "__main__":
    verify()
