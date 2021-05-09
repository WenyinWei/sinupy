"""Medium Class & The Classes Derived from It

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

from sympy import Symbol as _Symbol 
from sympy import Matrix as _Matrix
from sympy import Eq as _Eq
from sympy import tensorcontraction as _tcontract
from sympy import tensorproduct as _tprod
m_dot_v = lambda a,b : _tcontract(_tprod(a, b), (1,2))

def c(): # light speed in vacuum 
    return _Symbol('c', positive=True)

class WaveEq(_Eq):
    def __new__(cls, medium, wave=None, *arg, **kwarg):
        from .waves import ElectroMagneticWave
        from ..algebra.tensor import m_A_x
        from ..mediums.plasma import relative_dielectric_tensor
        if wave is None:
            wave = ElectroMagneticWave() 
        m_vk_x = m_A_x(wave.k)
        obj = super(_Eq, cls).__new__(cls,
            m_dot_v(m_vk_x, m_dot_v(m_vk_x, wave.E)), 
            - (wave.w/c())**2 * m_dot_v(
                relative_dielectric_tensor(medium), 
                wave.E), *arg, **kwarg)
        obj.medium = medium
        obj.wave = wave
        return obj

    def coeff_matrix(self):
        from ..algebra.tensor import m_A_x
        from ..mediums.plasma import relative_dielectric_tensor
        m_vk_x = m_A_x(self.wave.k)
        return m_vk_x.tomatrix() * m_vk_x.tomatrix() + (self.wave.w / c())**2 * relative_dielectric_tensor(self.medium)
    
def theta_btwn_B_and_k(wave_eq):
    from ..mediums import MagnetizedPlasma
    assert(isinstance(wave_eq.medium, MagnetizedPlasma))
    return _Symbol('theta', nonnegative=True)
    

def solve_N2(wave_eq, theta=None): # Express N**2, the square of the wave's relative refraction index, with theta and kappa symbols.
    from sympy import solve, Eq
    from sympy import sin, cos
    det = wave_eq.coeff_matrix().det()
    wave = wave_eq.wave
    from ..mediums import MagnetizedPlasma
    if isinstance(wave_eq.medium, MagnetizedPlasma):
        theta_ = theta_btwn_B_and_k(wave_eq) if theta is None else theta
        det = det.subs(wave.k[1], 0) # set k_y to 0
        det = det.subs(wave.k[0], wave.k_amp() * sin(theta_)) # set k_x to k_amp * sin(theta)
        det = det.subs(wave.k[2], wave.k_amp() * cos(theta_)) # set k_z to k_amp * cos(theta)
        N = wave.relative_refraction_N()
        det = det.subs(wave.k_amp(), wave.w / c() * N)
        N2_sol = solve(Eq(det.simplify(), 0), (N**2))
        if theta is None:
            return [sol.simplify() for sol in N2_sol]
        else:
            from ..algebra.quadratic import simplify_quadratic_sols
            return list(simplify_quadratic_sols(N2_sol[0], N2_sol[1]))
    else:
        raise NotImplementedError()


