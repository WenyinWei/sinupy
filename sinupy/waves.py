
from sympy import Symbol as _Symbol 
from sympy import symbols as _symbols
from sympy import Array as _Array

class Wave:
    def __init__(self, k=None, w=None):
        if k is None:   
            k_x, k_y, k_z, k = _symbols('k_x, k_y, k_z, k', complex=True)
            self.k = _Array([k_x, k_y, k_z])
        else:
            self.k = k
        if w is None: 
            self.w = _Symbol('omega') 
        else:
            self.w = w


class ElectroMagneticWave(Wave):
    def __init__(self, E=None, B=None):
        self.E = E
        self.B = B

class ElectrostaticWave(Wave):
    def __init__(self, E=None):
        self.E = E

