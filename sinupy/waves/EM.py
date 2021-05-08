"""Medium Class & The Classes Derived from It

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

from sympy import Symbol as _Symbol 
from sympy import Matrix as _Matrix
from sympy import Eq as _Eq

class WaveEq(_Eq):
    def __init__(self, medium, wave=None, *arg, **kwarg):
        from .waves import Wave
        # super().__init__(wave.k cross (wave.k cross E) + (wave.w/c())**2 (kappa_tensor_p dot E), 0)
        self.medium = medium 
        self.wave = Wave() if wave is None else wave
    
    def coeff_tensor(self):
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
    from .waves import c
    det = wave_eq.coeff_tensor().det()
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


