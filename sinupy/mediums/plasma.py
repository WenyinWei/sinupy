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

def omega_pe(plasma=None):
    return _Symbol('\omega_{pe}', negative=False)
def omega_ce(magnetized_plasma=None):
    return _Symbol('\omega_{ce}', negative=False)
def omega_pi(plasma=None):
    return _Symbol('\omega_{pi}', negative=False)
def omega_ci(magnetized_plasma=None):
    return _Symbol('\omega_{ci}', negative=False)

def kappa2omega(expr, wave, plasma=None):
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
    from sinupy.waves.EM import kappa_para, kappa_perp, kappa_times
    f = lambda a,b,c: a**2 / (b**2 - c**2)
    if plasma.species == 'electron':
        w, w_pe, w_ce = wave.omega, omega_pe(plasma), omega_ce(plasma)
        expr = expr\
            .subs(kappa_perp(plasma), 1 - f(w_pe, w, w_ce))\
            .subs(kappa_times(plasma), (w_ce / w) * f(w_pe, w, w_ce))\
            .subs(kappa_para(plasma), 1 - w_pe**2 / w**2 ) 
    elif plasma.species == 'electron+ion':
        w, w_pe, w_ce, w_pi, w_ci = wave.omega, omega_pe(plasma), omega_ce(plasma), omega_pi(plasma), omega_ci(plasma)
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
