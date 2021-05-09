
from sympy import Symbol as _Symbol 
from sympy import symbols as _symbols
from sympy import Array as _Array

class Wave:
    def __init__(self, varidx='', k=None, w=None):
        self.varidx = varidx
        if k is None:   
            k_x, k_y, k_z= _symbols('k_x_{varidx}, k_y_{varidx}, k_z_{varidx}'.format(varidx=self.varidx), complex=True)
            self.k = _Array([k_x, k_y, k_z])
        else:
            self.k = k

        if w is None: 
            self.w = _Symbol('omega_{varidx}'.format(varidx=self.varidx), complex=True) 
        else:
            self.w = w
    def k_amp(self):
        return _Symbol('k_{amp}_{varidx}'.format(amp='amp', varidx=self.varidx), negative=False)
    def w_amp(self):
        return _Symbol('w_{amp}_{varidx}'.format(amp='amp', varidx=self.varidx), negative=False)


# Waves involved in electrodynamics
class ElectroMagneticWave(Wave):
    def __init__(self, E=None, B=None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        if E is None: 
            E_x, E_y, E_z = _symbols('E_x_{varidx}, E_y_{varidx}, E_z_{varidx}'.format(varidx=self.varidx), complex=True)
            self.E = _Array([E_x, E_y, E_z])
        else:
            self.E = E

        if B is None: 
            B_x, B_y, B_z = _symbols('B_x_{varidx}, B_y_{varidx}, B_z_{varidx}'.format(varidx=self.varidx), complex=True)
            self.B = _Array([B_x, B_y, B_z])
        else:
            self.B = B

    def E_amp(self):
        return _Symbol('E_{amp}_{varidx}'.format(amp='amp', varidx=self.varidx), negative=False)
    def B_amp(self):
        return _Symbol('B_{amp}_{varidx}'.format(amp='amp', varidx=self.varidx), negative=False)
    def relative_refraction_N(self):
        return _Symbol('N_{varidx}'.format(varidx=self.varidx))

class ElectrostaticWave(ElectroMagneticWave):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

def makeWave(k=None, w=None, u=None, E=None, B=None):
    pass