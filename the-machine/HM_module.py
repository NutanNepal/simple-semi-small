import sys
import os
# Get the parent directory of the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

# Import SageMath and custom functions
from custom_matroid_functions import *
from sage.combinat.posets.moebius_algebra import *
from sage.matroids.constructor import Matroid
from sage.combinat.free_module import CombinatorialFreeModule
from sage.rings.polynomial.laurent_polynomial_ring import LaurentPolynomialRing
from sage.rings.integer_ring import ZZ

class ChowBasis(BasisAbstract):
    """
    The Chow basis for the Deformed Möbius Algebra (Chow ring context).
    """
    def __init__(self, M, prefix='C') -> None:
        self._basis_name = "chow"
        # The basis could be indexed by flags, or by certain monomials in x_F
        # For now, let's assume it's indexed by flats (like the zeta basis)
        CombinatorialFreeModule.__init__(self, M.base_ring(),
                                        tuple(M._lattice),
                                        prefix=prefix,
                                        category=MoebiusAlgebraBases(M))

        # Change of basis:
        E = M.E()
        phi = self.module_morphism(self._to_natural_basis,
                                codomain=E, category=self.category(),
                                triangular='upper', unitriangular=True,
                                key=M._lattice._element_to_vertex)

        phi.register_as_coercion()
        (~phi).register_as_coercion()

    def _to_natural_basis(self, F):
        M = self.realization_of()
        L = M._lattice
        E = M.E()
        q = M._q
        kl = lambda y, x: L.kazhdan_lusztig_polynomial(y, x)
        rank = L.rank_function()
        matroid = M._matroid
        R = M.base_ring()
        # For each G ≤ F, get the Poincaré polynomial of the contraction M^F_G
        return E.sum_of_terms(
            (G, q**(1 * (rank(F) - rank(G))) *
            R(poincare_polynomial_of_minor(matroid, F, G)(q**-2)))
            #R(-reduced_characteristic_polynomial_of_minor(matroid, F, G)(q**-2)))
            #R(characteristic_polynomial(matroid.delete(matroid.groundset() - F).contract(G))(q**-2)))
            #R(inverse_kazhdan_lustig_polynomial(matroid.delete(matroid.groundset() - F).contract(G))(q**-2)))
            #kl(G, F)(q=q**-2))
            for G in L.order_ideal([F])
        )

class ZetaBasis(BasisAbstract):
    """
    The zeta basis for the Quantum Möbius Algebra.
    """
    def __init__(self, M, prefix='Z') -> None:
        self._basis_name = "zeta"
        CombinatorialFreeModule.__init__(self, M.base_ring(),
                                        tuple(M._lattice),
                                        prefix=prefix,
                                        category=MoebiusAlgebraBases(M))

        # Change of basis:
        E = M.E()
        phi = self.module_morphism(self._to_natural_basis,
                                codomain=E, category=self.category(),
                                triangular='upper', unitriangular=True,
                                key=M._lattice._element_to_vertex)

        phi.register_as_coercion()
        (~phi).register_as_coercion()

    def _to_natural_basis(self, x):
        M = self.realization_of()
        L = M._lattice
        E = M.E()
        q = M._q
        rank = L.rank_function()
        R = M.base_ring()
        return E.sum_of_terms(
            (y, q**(rank(x) - rank(y)) * R(L.kazhdan_lusztig_polynomial(y, x)(q=q**-2)))
            for y in L.order_ideal([x])
        )

class invFBasis(BasisAbstract):
    """
    The invF basis for the Quantum Möbius Algebra.
    """
    def __init__(self, M, prefix='invF') -> None:
        self._basis_name = "invF"
        CombinatorialFreeModule.__init__(self, M.base_ring(),
                                        tuple(M._lattice),
                                        prefix=prefix,
                                        category=MoebiusAlgebraBases(M))

        # Change of basis:
        E = M.E()
        phi = self.module_morphism(self._to_natural_basis,
                                codomain=E, category=self.category(),
                                triangular='upper', unitriangular=True,
                                key=M._lattice._element_to_vertex)

        phi.register_as_coercion()
        (~phi).register_as_coercion()

    def _to_natural_basis(self, x):
        M = self.realization_of()
        L = M._lattice
        E = M.E()
        q = M._q
        rank = L.rank_function()
        matroid = M._matroid
        R = M.base_ring()
        mu_rev_x = convolve(rev(mu), convolve(chow_polynomial, rev(kl_poly)))
        res = E.sum_of_terms(
            (G, q**(rank(x) - rank(G)) * R(mu_rev_x(matroid.delete(matroid.groundset() - x).contract(G)))(q**-2))
            for G in L.order_ideal([x])
        )
        return res

class MuBasis(BasisAbstract):
    """
    The mu basis for the Quantum Möbius Algebra.
    """
    def __init__(self, M, prefix='mu') -> None:
        self._basis_name = "mu"
        CombinatorialFreeModule.__init__(self, M.base_ring(),
                                        tuple(M._lattice),
                                        prefix=prefix,
                                        category=MoebiusAlgebraBases(M))

        # Change of basis:
        E = M.E()
        phi = self.module_morphism(self._to_natural_basis,
                                codomain=E, category=self.category(),
                                triangular='upper', unitriangular=True,
                                key=M._lattice._element_to_vertex)

        phi.register_as_coercion()
        (~phi).register_as_coercion()

    def _to_natural_basis(self, F):
        M = self.realization_of()
        L = M._lattice
        E = M.E()
        q = M._q
        rank = L.rank_function()
        matroid = M._matroid
        R = M.base_ring()
        
        # mu^F = sum_{G <= F} x^{g-f} * mu(M^F_G) * G
        # Therefore x^{g-f} corresponds to q^{rank(G) - rank(F)} (keeping in mind q = x, though in the module q represents the parameter).
        # We need the mu polynomial (characteristic polynomial evaluated at 0).
        def mu_val(m_matroid):
            from custom_matroid_functions import characteristic_polynomial
            return characteristic_polynomial(m_matroid)(0)
            
        res = E.sum_of_terms(
            (G, q**(rank(G) - rank(F)) * R(mu_val(matroid.delete(matroid.groundset() - F).contract(G))))
            for G in L.order_ideal([F])
        )
        return res

class DeformedMoebiusAlgebra(QuantumMoebiusAlgebra):
    """
    A class representing the Deformed Möbius Algebra with the Zeta basis.
    Can be constructed from either a matroid or a lattice of flats.
    """
    def __init__(self, matroid, base_ring=None):
        """
        Initialize the Deformed Möbius Algebra from a matroid.
        The lattice of flats is automatically extracted from the matroid.
        """
        if base_ring is None:
            self._R = LaurentPolynomialRing(ZZ, 'x')
        else:
            self._R = base_ring
        x = self._R.gen()

        # Store the matroid and get its lattice of flats
        self._matroid = matroid
        self._lattice = matroid.lattice_of_flats()

        super().__init__(self._lattice, x)
        self._chow_basis = ChowBasis(self)
        self._zeta_basis = ZetaBasis(self)
        self._invF_basis = invFBasis(self)
        self._mu_basis = MuBasis(self)

    def C(self):
        """
        Returns the Chow basis for this algebra.
        """
        return self._chow_basis

    def zeta(self):
        """
        Return the zeta basis for this algebra.
        """
        return self._zeta_basis

    def invF(self):
        """
        Return the invF basis for this algebra.
        """
        return self._invF_basis

    def mu(self):
        """
        Return the mu basis for this algebra.
        """
        return self._mu_basis

    def is_in_Hp(self, alpha):
        """
        Check if an element alpha belongs to the space H_p.
        
        INPUT:
        - alpha: an element of the algebra
        
        OUTPUT:
        - True if alpha is in H_p, False otherwise
        
        The space H_p consists of elements that satisfy
        certain palindromic conditions with respect to the lattice structure.
        For perverse elements, we check that the coefficients are palindromic
        with respect to the rank differences.
        """
        E = self.E()
        L = self._lattice
        t = self._q
        rank_func = L.rank_function()
        
        alpha_dict = E(alpha).monomial_coefficients()
        
        for F in alpha_dict.keys():
            """
            try:
                alpha_dict[F].subs({t: 0})
            except (TypeError, ValueError, ZeroDivisionError):
                print(f"Coefficient for F={F} is not a polynomial: {alpha_dict[F]}")
                return False
            """

            sum_S_F = 0
            rank_F = rank_func(F)

            for G in L.order_filter([F]):
                coeff_G = alpha_dict.get(G, 0) # Get coefficient alpha_G, default to 0
                if coeff_G != 0:
                    rank_G = rank_func(G)
                    term = coeff_G * (t**(1 * (rank_F - rank_G)))
                    sum_S_F += term
            try:
                # Check if the sum is palindromic (invariant under t -> 1/t)
                if sum_S_F != sum_S_F.subs({t: 1/t}):
                    print(f"Palindromic check failed for F={F}")
                    print(f"Sum = {sum_S_F}")
                    print(f"Sum(1/t) = {sum_S_F.subs({t: 1/t})}")
                    return False
            except Exception as e:
                print(f"Error during palindromic check for F={F}: {e}")
                return False

        return True

# Utility functions for working with the algebra
def create_deformed_algebra(matroid, base_ring=None):
    """
    Create a DeformedMoebiusAlgebra from a matroid.
    
    INPUT:
    - matroid: a SageMath matroid
    - base_ring: optional base ring (default: LaurentPolynomialRing(ZZ, 'x'))
    
    OUTPUT:
    - DeformedMoebiusAlgebra instance
    """
    return DeformedMoebiusAlgebra(matroid, base_ring=base_ring)

def create_deformed_algebra_from_lattice(lattice, base_ring=None):
    """
    Create a DeformedMoebiusAlgebra from a lattice of flats.
    
    INPUT:
    - lattice: a lattice of flats
    - base_ring: optional base ring (default: LaurentPolynomialRing(ZZ, 'x'))
    
    OUTPUT:
    - DeformedMoebiusAlgebra instance
    """
    matroid = Matroid(lattice)
    return DeformedMoebiusAlgebra(matroid, base_ring=base_ring)

# Define what should be imported when using "from HM_module import *"
__all__ = [
    'ChowBasis',
    'ZetaBasis', 
    'invFBasis',
    'MuBasis',
    'DeformedMoebiusAlgebra',
    'create_deformed_algebra',
    'create_deformed_algebra_from_lattice'
]