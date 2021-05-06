"""Algebra utilities involved in the deduction procedure of fusion plasma physics formula.

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

from sympy import Array as _Array
from sympy import LeviCivita as _LeviCivita
from sympy import tensorcontraction as _tcontract
from sympy import tensorproduct as _tprod

# t_LC means a LeviCivita *t*ensor.
t_LC = _Array([[[_LeviCivita(i1+1,i2+1,i3+1) for i3 in range(3)] for i2 in range(3)] for i1 in range(3)])

def cross(A, B):
    _tcontract(_tprod(A, B, t_LC),(0,2),(1,3))

def dot(A, B):
    # TODO
    pass 

def m_A_x(A):
    """returns a matrix Array equivalent with $\vec{A} \times$ operation, where $\vec{A}$ is a vector while $\times$ is cross product.  

    Args:
        A (sympy.Array): A should be a vector

    Returns:
        sympy.Array: A Matrix equivalent with $\vec{A} \times$ operation.
    """
    return _tcontract(_tprod(t_LC, A), (1,3))
