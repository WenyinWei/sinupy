"""Medium Class & The Classes Derived from It

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

from sympy import Symbol as _Symbol 
from sympy import Matrix as _Matrix

def tensor_in_wave_equation(plasma, wave):
    from sinupy.algebra.tensor import m_A_x
    m_vk_x = m_A_x(wave.k)
    return m_vk_x.tomatrix() * m_vk_x.tomatrix() + wave.k_0**2 * wave.relative_dielectric_tensor() 

def solve_N2_with_theta_and_kappa_component(cls):
    from sympy import solve, Eq
    tensor_det_in_wave_equation = cls.tensor_in_wave_equation().det()
    tensor_det_in_wave_equation_with_k_0_and_N = \
        cls.subs_k_with_k_0_and_N(
            cls.subs_k_component_with_k_theta(
                tensor_det_in_wave_equation))
    N2_sol = solve(Eq(tensor_det_in_wave_equation_with_k_0_and_N.simplify(), 0), (cls.N**2))
    return [sol.simplify() for sol in N2_sol]

def solve_N2_with_specific_theta_and_kappa_component(cls, theta_value):
    from sinupy.algebra.quadratic import simplify_quadratic_sols
    N2_with_specific_theta_and_kappa_component_ = [
            cls.set_theta_value(sol, theta_value) 
        for sol in cls.solve_N2_with_theta_and_kappa_component()]
    return list(simplify_quadratic_sols(
        N2_with_specific_theta_and_kappa_component_[0],
        N2_with_specific_theta_and_kappa_component_[1]))

