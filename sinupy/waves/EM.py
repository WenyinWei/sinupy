"""Medium Class & The Classes Derived from It

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

from sympy import Symbol as _Symbol 
from sympy import Matrix as _Matrix

# The components in relative dielectric tensor 
def kappa_para(magnetized_plasma=None):
    return _Symbol('kappa_\parallel', real=True)
def kappa_times(magnetized_plasma=None):
    return _Symbol('\kappa_{\\times}', real=True)
def kappa_perp(magnetized_plasma=None):
    return _Symbol('kappa_\perp', real=True)
def relative_dielectric_tensor(plasma=None): # The tensor's symbols is kappa 
    from sympy import I
    from ..mediums import MagnetizedPlasma
    if isinstance(plasma, MagnetizedPlasma):
        return _Matrix([
            [kappa_perp(plasma),    -I*kappa_times(plasma), 0                   ],
            [I*kappa_times(plasma), kappa_perp(plasma),     0                   ],
            [0,                                0,           kappa_para(plasma)  ]])
def relative_refraction_N(plasma, wave):
    return _Symbol('N')

def k_0(electromagnetic_wave):
    # from sinupy.waves import ElectroMagneticWave
    # if isinstance(electromagnetic_wave, ElectroMagneticWave):    
    return _Symbol('k_0', positive=True)

def wave_from_wave_equation(plasma=None):
    from .waves import Wave
    return Wave()

def theta_between_B_and_k(plasma, wave):
    return _Symbol('theta', nonnegative=True)

def tensor_in_wave_equation(plasma, wave):
    from ..algebra.tensor import m_A_x
    wave = wave_from_wave_equation()
    m_vk_x = m_A_x(wave.k)
    return m_vk_x.tomatrix() * m_vk_x.tomatrix() + k_0(wave)**2 * relative_dielectric_tensor(plasma) 

def N2_with_theta_and_kappa_component_via_det_equal_zero(plasma, wave):
    from sympy import solve, Eq
    from sympy import sin, cos
    det = tensor_in_wave_equation(plasma, wave).det()
    wave = wave_from_wave_equation() if wave is None else wave
    det = det.subs(wave.k[1], 0) # set k_y to 0
    theta = theta_between_B_and_k(plasma, wave) 
    det = det.subs(wave.k[0], wave.k_amp() * sin(theta)) # set k_x to k_amp * sin(theta)
    det = det.subs(wave.k[2], wave.k_amp() * cos(theta)) # set k_z to k_amp * cos(theta)
    N = relative_refraction_N(plasma, wave)
    det = det.subs(wave.k_amp(), k_0(wave) * N)
    N2_sol = solve(Eq(det.simplify(), 0), (N**2))
    return [sol.simplify() for sol in N2_sol]


def N2_with_specific_theta_and_kappa_component_via_det_equal_zero(plasma, wave, theta_value):
    from ..algebra.quadratic import simplify_quadratic_sols
    theta = theta_between_B_and_k(plasma, wave)
    N2_with_specific_theta_and_kappa_component_ = [
            sol.subs(theta, theta_value) 
        for sol in N2_with_theta_and_kappa_component_via_det_equal_zero(plasma, wave)]
    return list(simplify_quadratic_sols(
        N2_with_specific_theta_and_kappa_component_[0],
        N2_with_specific_theta_and_kappa_component_[1]))

