"""Some Parameters of Plasma

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

import sinupy.mediums as _mediums

from sympy import Symbol as _Symbol 
from sympy import symbols as _symbols
from sympy import Array as _Array
from sympy import Matrix as _Matrix
from sympy import LeviCivita as _LeviCivita
from sympy import tensorcontraction as _tcontract
from sympy import tensorproduct as _tprod
from sinupy.algebra.utility import run_once

# The components in relative dielectric tensor 
def kappa_para(magnetized_plasma=None):
    return _Symbol('kappa_\parallel', real=True)
def kappa_times(magnetized_plasma=None):
    return _Symbol('\kappa_{\\times}', real=True)
def kappa_perp(magnetized_plasma=None):
    return _Symbol('kappa_\perp', real=True)
def relative_dielectric_tensor(magnetized_plasma=None): # The tensor's symbols is kappa 
    from sympy import I
    return _Matrix([
        [kappa_perp(magnetized_plasma),    -I*kappa_times(magnetized_plasma), 0],
        [I*kappa_times(magnetized_plasma), kappa_perp(magnetized_plasma),     0],
        [0,                                0,                                 kappa_para(magnetized_plasma)]])

def omega_pe(plasma=None):
    return _Symbol('\omega_{pe}', negative=False)
def omega_ce(magnetized_plasma=None):
    return _Symbol('\omega_{ce}', negative=False)
def omega_pi(plasma=None):
    return _Symbol('\omega_{pi}', negative=False)
def omega_ci(magnetized_plasma=None):
    return _Symbol('\omega_{ci}', negative=False)

def subs_kappa_with_omega(expr, plasma=None):
    """Substitute kappa components with various omega -- characteristic (angular) frequency in plasma.

    Args:
        expr (sympy.expr): The sympy expression which contains kappa components (kappa_para, kappa_times, kappa_perp) 
        species (str, optional): [description]. Defaults to 'electron'.

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]

    DevNote:
        Do not try to simplify the expression! The expression can be so complicated that a lot of time would be wasted to get a nonsense.

    """
    f = lambda a,b,c: a**2 / (b**2 - c**2)
    if plasma.species == 'electron':
        o, o_pe, o_ce = cls.omega, omega_pe(plasma), omega_ce(plasma)
        expr = expr\
            .subs(kappa_perp, 1 - f(o_pe, o, o_ce))\
            .subs(kappa_times, (o_ce / o) * f(o_pe, o, o_ce))\
            .subs(kappa_para, 1 - o_pe**2 / o**2 ) 
    elif plasma.species == 'electron+ion':
        w, w_pe, w_ce, w_pi, w_ci = cls.omega, omega_pe(plasma), omega_ce(plasma), omega_pi(plasma), omega_ci(plasma)
        expr = expr\
            .subs(kappa_perp(plasma), 
                1 - f(w_pe, w, w_ce) - f(w_pi, w, w_ci))\
            .subs(kappa_times(plasma), 
                w_ce/w * f(w_pe, w, w_ce) - w_ci/w * f(w_pi, w, w_ci))\
            .subs(kappa_para(plasma),
                1 - w_pe**2/w**2)
    else:
        raise ValueError("Not yet prepared for this kind of composite species of plasma -- {plasma.species}. ")
    return expr
