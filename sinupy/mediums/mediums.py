"""Medium Class & The Classes Derived from It

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

from sympy import Symbol as _Symbol 
from sympy import symbols as _symbols
from sympy import Array as _Array
from sympy import Matrix as _Matrix
from sympy import LeviCivita as _LeviCivita

class Medium:
    def __init__(self):
        pass


class Solid(Medium):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
    

class Liquid(Medium):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
    

class Gas(Medium):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
    

class Plasma(Medium):

    def __init__(self, species='e', *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.species = set(species.split('+'))
        self.n = {s: _symbols(f'n_{s}', nonnegative=True) for s in self.species}
        self.m = {s: _symbols(f'm_{s}', nonnegative=True) for s in self.species}
class WarmPlasma(Plasma):
    
    def __init__(self, T=None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
    
        if T is None:
            self.T = _Symbol('T')
        else:
            self.T = 0
    
class ColdPlasma(WarmPlasma):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
    

class MagnetizedPlasma(Plasma):
    def __init__(self, B=None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
    
        if B is None:
            B_x, B_y, B_z = _symbols('B_x, B_y, B_z')
            self.B = _Array([B_x, B_y, B_z])
        else:
            self.B = B

    def B_amp(self):
        return _symbols('B^{static}_{amp}', negative=False)

class WarmMagnetizedPlasma(WarmPlasma, MagnetizedPlasma):

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
    
class ColdMagnetizedPlasma(ColdPlasma, MagnetizedPlasma):

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
    

def makePlasma(Maxwell=True, f=None, B=None, T=None):
    if Maxwell:
        if B is not None:
            return WarmMagnetizedPlasma()
        else:
            return WarmPlasma()
    elif not Maxwell:
        if B is not None:
            return MagnetizedPlasma()
        else:
            return Plasma()
    