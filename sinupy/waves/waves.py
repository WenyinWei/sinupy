
from sympy import Symbol as _Symbol 
from sympy import symbols as _symbols
from sympy import Array as _Array

class Wave:
    def __init__(self, k=None, w=None):

        if k is None:   
            k_x, k_y, k_z= _symbols('k_x, k_y, k_z', complex=True)
            self.k = _Array([k_x, k_y, k_z])
        else:
            self.k = k

        if w is None: 
            self.w = _Symbol('omega', complex=True) 
        else:
            self.w = w
    def k_amp(self):
        return _Symbol('k_{amp}', negative=False)
    def w_amp(self):
        return _Symbol('w_{amp}', negative=False)

class ElectroMagneticWave(Wave):
    def __init__(self, E=None, B=None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        if E is None: 
            E_x, E_y, E_z = _symbols('E_x, E_y, E_z', complex=True)
            self.E = _Array([E_x, E_y, E_z])
        else:
            self.E = E

        if B is None: 
            B_x, B_y, B_z = _symbols('B_x, B_y, B_z', complex=True)
            self.B = _Array([B_x, B_y, B_z])
        else:
            self.B = B
    def E_amp(self):
        return _Symbol('E_{amp}', negative=False)
    def B_amp(self):
        return _Symbol('B_{amp}', negative=False)

class ElectrostaticWave(Wave):
    def __init__(self, E=None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        if E is None: 
            E_x, E_y, E_z = _symbols('E_x, E_y, E_z', complex=True)
            self.E = _Array([E_x, E_y, E_z])
        else:
            self.E = E

    def E_amp(self):
        return _Symbol('E_{amp}', negative=False)

def makeWave(k=None, w=None, u=None, E=None, B=None):
    pass