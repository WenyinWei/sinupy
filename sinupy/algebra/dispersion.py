"""Algebra utilities involved in the deduction procedure of fusion plasma physics formula.

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

class deduction_dispersion_in_plasma:

    k_0 = _Symbol('k_0', positive=True)
    theta = _Symbol('theta', nonnegative=True)
    N = _Symbol('N')
    k_x, k_y, k_z, k = _symbols('k_x, k_y, k_z, k', real=True); vk = _Array([k_x, k_y, k_z])
    omega, omega_pe, omega_ce, omega_pi, omega_ci = _symbols(
        'omega, \omega_{pe}, \omega_{ce}, \omega_{pi}, \omega_{ci}', negative=False)
    E_x, E_y, E_z = _symbols('E_x, E_y, E_z'); vE = _Array([E_x, E_y, E_z])
    kappa_para, kappa_times, kappa_perp = _symbols('kappa_\parallel, \kappa_{\\times}, kappa_\perp', real=True)
    B = _Symbol('B')
    n_e, n_i = _symbols('n_e, n_i')

    @classmethod
    def relative_dielectric_tensor(cls):
        from sympy import I
        return _Matrix([
            [cls.kappa_perp,    -I*cls.kappa_times, 0],
            [I*cls.kappa_times, cls.kappa_perp,     0],
            [0,                 0,     cls.kappa_para]])

    @classmethod
    def tensor_in_wave_equation(cls):
        from sinupy.algebra.tensor import m_A_x
        m_vk_x = m_A_x(cls.vk)
        return m_vk_x.tomatrix() * m_vk_x.tomatrix() + cls.k_0**2 * cls.relative_dielectric_tensor() 

    @classmethod
    def subs_k_component_with_k_theta(cls, expr):
        from sympy import sin, cos
        expr = expr.subs(cls.k_y, 0)
        expr = expr.subs(cls.k_x, cls.k* sin(cls.theta)).subs(cls.k_z, cls.k*cos(cls.theta))
        return expr

    @classmethod
    def subs_k_with_k_0_and_N(cls, expr):
        return expr.subs(cls.k, cls.k_0 * cls.N)

    @classmethod
    def set_theta_value(cls, expr, theta_value):
        return expr.subs(cls.theta, theta_value)

    # @classmethod
    # def solve_N2_with_theta(cls, theta_value):
    #     N2_sol_theta_ = [sol.subs(theta, theta_value).simplify() for sol in N2_sol]
    #     return list(fuquad.simplify_quadratic_sols(N2_sol_theta_[0], N2_sol_theta_[1]))

    @classmethod
    @run_once
    def solve_N2_with_theta_and_kappa_component(cls):
        from sympy import solve, Eq
        tensor_det_in_wave_equation = cls.tensor_in_wave_equation().det()
        tensor_det_in_wave_equation_with_k_0_and_N = \
            cls.subs_k_with_k_0_and_N(
                cls.subs_k_component_with_k_theta(
                    tensor_det_in_wave_equation))
        N2_sol = solve(Eq(tensor_det_in_wave_equation_with_k_0_and_N.simplify(), 0), (cls.N**2))
        return [sol.simplify() for sol in N2_sol]
    
    @classmethod
    def solve_N2_with_specific_theta_and_kappa_component(cls, theta_value):
        from sinupy.algebra.quadratic import simplify_quadratic_sols
        N2_with_specific_theta_and_kappa_component_ = [
                cls.set_theta_value(sol, theta_value) 
            for sol in cls.solve_N2_with_theta_and_kappa_component()]
        return list(simplify_quadratic_sols(
            N2_with_specific_theta_and_kappa_component_[0],
            N2_with_specific_theta_and_kappa_component_[1]))

    @classmethod
    def subs_kappa_with_omega(cls, expr, plasma_type='electron'):
        """Substitute kappa_components with omega components.

        Args:
            expr (sympy.expr): [description]
            plasma_type (str, optional): [description]. Defaults to 'electron'.

        Raises:
            ValueError: [description]

        Returns:
            [type]: [description]

        DevNote:
            Do not try to simplify the expression! The expression can be so complicated that a lot of time would be wasted to get a nonsense.

        """
        f = lambda a,b,c: a**2 / (b**2 - c**2)
        if plasma_type == 'electron':
            o, o_pe, o_ce = cls.omega, cls.omega_pe, cls.omega_ce
            expr = expr\
                .subs(cls.kappa_perp, 1 - f(o_pe, o, o_ce))\
                .subs(cls.kappa_times, (o_ce / o) * f(o_pe, o, o_ce))\
                .subs(cls.kappa_para, 1 - o_pe**2 / o**2 ) 
        elif plasma_type == 'electron+ion':
            o, o_pe, o_ce, o_pi, o_ci = cls.omega, cls.omega_pe, cls.omega_ce, cls.omega_pi, cls.omega_ci
            expr = expr\
                .subs(cls.kappa_perp, 
                    1 - f(o_pe, o, o_ce) - f(o_pi, o, o_ci))\
                .subs(cls.kappa_times, 
                    o_ce/o * f(o_pe, o, o_ce) - o_ci/o * f(o_pi, o, o_ci))\
                .subs(cls.kappa_para,
                    1 - o_pe**2/o**2)
        else:
            raise ValueError("Unprepared plasma type")
        return expr

