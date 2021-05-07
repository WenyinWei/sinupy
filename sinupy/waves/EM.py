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
def relative_dielectric_tensor(magnetized_plasma=None): # The tensor's symbols is kappa 
    from sympy import I
    return _Matrix([
        [kappa_perp(magnetized_plasma),    -I*kappa_times(magnetized_plasma), 0],
        [I*kappa_times(magnetized_plasma), kappa_perp(magnetized_plasma),     0],
        [0,                                0,                                 kappa_para(magnetized_plasma)]])
def relative_refraction_N(plasma):
    return _Symbol('N')

def tensor_in_wave_equation(plasma, wave):
    from sinupy.algebra.tensor import m_A_x
    m_vk_x = m_A_x(wave.k)
    return m_vk_x.tomatrix() * m_vk_x.tomatrix() + wave.k_0**2 * relative_dielectric_tensor(plasma) 

def solve_N2_with_theta_and_kappa_component(plasma):
    from sympy import solve, Eq
    tensor_det_in_wave_equation = tensor_in_wave_equation(plasma).det()
    tensor_det_in_wave_equation_with_k_0_and_N = \
        subs_k_with_k_0_and_N(
            subs_k_component_with_k_theta(
                tensor_det_in_wave_equation))
    N2_sol = solve(Eq(tensor_det_in_wave_equation_with_k_0_and_N.simplify(), 0), (plasma.N**2))
    return [sol.simplify() for sol in N2_sol]

def solve_N2_with_specific_theta_and_kappa_component(theta_value):
    from sinupy.algebra.quadratic import simplify_quadratic_sols
    N2_with_specific_theta_and_kappa_component_ = [
            sol.subs(theta, theta_value) 
        for sol in solve_N2_with_theta_and_kappa_component()]
    return list(simplify_quadratic_sols(
        N2_with_specific_theta_and_kappa_component_[0],
        N2_with_specific_theta_and_kappa_component_[1]))

