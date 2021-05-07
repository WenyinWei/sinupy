"""Medium Class & The Classes Derived from It

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

from sympy import Symbol as _Symbol 
from sympy import symbols as _symbols
from sympy import Array as _Array
from sympy import Matrix as _Matrix
from sympy import LeviCivita as _LeviCivita
from sympy import tensorcontraction as _tcontract
from sympy import tensorproduct as _tprod
from sinupy.algebra.utility import run_once

class Medium:
    def __init__(self, name="Unknown Medium"):
        if name: self.name = name


class Solid(Medium):
    def __init__(self):
        pass

class Liquid(Medium):
    def __init__(self):
        pass

class Gas(Medium):
    def __init__(self):
        pass

class Plasma(Medium):

    def __init__(self, species='e'):
        super().__init__()
        self.n_e, self.n_i = _symbols('n_e, n_i', nonnegative=True)
        self.species = species
        if species=='e':
            self.n_e = _symbols('n_e', nonnegative=True)
            self.n_species = (self.n_e)
        elif species=='e+i':
            self.n_e, self.n_i = _symbols('n_e, n_i', nonnegative=True)
            self.n_species = (self.n_e, self.n_i)

class WarmPlasma(Plasma):
    
    def __init__(self, T=None):
        if T is None:
            self.T = _Symbol('T')
        else:
            self.T = 0
        super().__init__()
    
    
class ColdPlasma(WarmPlasma):
    def __init__(self, T=None):
        pass

class MagnetizedPlasma(Plasma):
    def __init__(self, B=None):
        if B is None:
            self.B = B
        else:
            B_x, B_y, B_z = _symbols('B_x, B_y, B_z')
            self.B = _Array([B_x, B_y, B_z])

class WarmMagnetizedPlasma(WarmPlasma, MagnetizedPlasma):

    def __init__(self):
        pass

class ColdMagnetizedPlasma(ColdPlasma, MagnetizedPlasma):

    def __init__(self):
        pass

def makePlasma(Maxwell=True, f=None, B=None, T=None):
    if Maxwell:
        if B is not None:
            return WarmMagnetizedPlasma()
        else B is None:
            return WarmPlasma()
    elif not Maxwell:
        if B is not None:
            return MagnetizedPlasma()
        elif B is None:
            return Plasma()
    