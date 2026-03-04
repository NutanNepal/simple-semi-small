"""
Custom Matroid Functions Package

This package contains custom implementations of matroid functions that extend
or fix functionality not available in the standard SageMath matroids module.

Main modules:
- core: Core utility functions and polynomial computations
- polynomials: Polynomial-specific functions for characteristic, KL, and Q polynomials
- chow_polynomials: Chow polynomial computations essential for Poincaré polynomial research
- extensions: Extended functionality for matroid operations
"""

from .core import cmp_elements_key, characteristic_polynomial, whitney_numbers
from .polynomials import (
    inverse_kazhdan_lustig_uniform, kazhdan_lustig_uniform, inverse_kazhdan_lustig_polynomial, invkl,
    kl_inverse_paving, kl_inverse_copaving, rev, convolve, mu, kl_poly
)
from .chow_polynomials import (
    chow_polynomial, get_chow_polynomial, reduced_characteristic_polynomial,
    reduced_characteristic_polynomial_of_minor,
    poincare_polynomial_of_minor,
    clear_chow_cache, get_chow_cache_info,
    save_chow_cache, export_chow_cache_to_csv
)
from .extensions import is_graphic, is_paving

__all__ = [
    # Core functions
    'cmp_elements_key', 'characteristic_polynomial', 'whitney_numbers',
    
    # Polynomial functions
    'inverse_kazhdan_lustig_uniform', 'kazhdan_lustig_uniform', 'inverse_kazhdan_lustig_polynomial', 'invkl',
    'kl_inverse_paving', 'kl_inverse_copaving', 'rev', 'convolve', 'mu', 'kl_poly',
    
    # Chow polynomial functions
    'chow_polynomial', 'get_chow_polynomial', 'reduced_characteristic_polynomial',
    'poincare_polynomial_of_minor',
    'clear_chow_cache', 'get_chow_cache_info',
    'save_chow_cache', 'export_chow_cache_to_csv', 'reduced_characteristic_polynomial_of_minor',
    
    # Extension functions
    'is_graphic', 'is_paving'
] 