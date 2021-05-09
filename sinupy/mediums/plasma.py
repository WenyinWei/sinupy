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


def omega_cj(
    q_e=None, 
    m=None, 
    B=None, magnetized_plasma=None, varidx='j'):
    from scipy.constants import e
    from sympy import Abs

    if any(v is not None for v in [q_e, m, B]):
        return _Abs(q_e) * e * B / m
    else:
        from .mediums import MagnetizedPlasma
        p = magnetized_plasma
        if isinstance(p, MagnetizedPlasma) or p is None:
            return _Symbol('\omega_{cj}'.format(pj=f'p{varidx}'), negative=False)
    
def omega_pj(
    n_0=None, 
    q_e=None, 
    m=None, plasma=None, varidx='j'):
    from scipy.constants import epsilon_0, e
    from sympy import sqrt

    if any(v is not None for [n_0, q_e, B]):
        return (q_e*_e) * sqrt( n_0 / (epsilon_0 * m) ) # Split the square of q_e * e, avoid it being too little
    else:
        from .mediums import Plasma
        if isinstance(plasma, Plasma) or plasma is None:
            return _Symbol('\omega_{pj}'.format(pj=f'p{varidx}'), negative=False)
 
def omega_ce(
    B=None, 
    magnetized_plasma=None):
    from scipy.constants import m_e
    return omega_cj(
        -1, m_e, B, 
        magnetized_plasma=magnetized_plasma, 
        varidx='e')
def omega_pe(
    n_0=None, 
    plasma=None):
    from scipy.constants import m_e
    return omega_pj(
        n_0, -1, m_e, B, 
        plasma=plasma, 
        varidx='e')


# The components in relative dielectric tensor 
def kappa_para(magnetized_plasma=None):
    return _Symbol('kappa_\parallel', real=True)
def kappa_times(magnetized_plasma=None):
    return _Symbol('\kappa_{\\times}', real=True)
def kappa_perp(magnetized_plasma=None):
    return _Symbol('kappa_\perp', real=True)
def relative_dielectric_tensor(plasma=None): # The tensor's symbols is kappa 
    from sympy import I
    from .mediums import MagnetizedPlasma

    if isinstance(plasma, MagnetizedPlasma):
        return _Matrix([
            [kappa_perp(plasma),    -I*kappa_times(plasma), 0                   ],
            [I*kappa_times(plasma), kappa_perp(plasma),     0                   ],
            [0,                                0,           kappa_para(plasma)  ]])
    else:
        raise NotImplementedError()

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
    f = lambda a,b,c: a**2 / (b**2 - c**2)
    if plasma.species == 'e':
        w, w_pe, w_ce = wave.omega, omega_pe(plasma), omega_ce(plasma)
        expr = expr\
            .subs(kappa_perp(plasma), 1 - f(w_pe, w, w_ce))\
            .subs(kappa_times(plasma), (w_ce / w) * f(w_pe, w, w_ce))\
            .subs(kappa_para(plasma), 1 - w_pe**2 / w**2 ) 
    elif plasma.species == 'e+i':
        w, w_pe, w_ce, w_pi, w_ci = wave.omega, omega_pe(plasma), omega_ce(plasma), omega_pi(plasma), omega_ci(plasma)
        expr = expr\
            .subs(kappa_perp(plasma), 
                1 - f(w_pe, w, w_ce) - f(w_pi, w, w_ci))\
            .subs(kappa_times(plasma), 
                w_ce/w * f(w_pe, w, w_ce) - w_ci/w * f(w_pi, w, w_ci))\
            .subs(kappa_para(plasma),
                1 - w_pe**2/w**2)
    else:
        raise NotImplementedError("Not yet prepared for this kind of composite species of plasma -- {plasma.species}. ")
    return expr