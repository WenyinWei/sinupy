from sympy import init_printing; init_printing()
from sympy import pi

from sinupy import mediums, waves
from sinupy.waves import EM, ElectroMagneticWave
from sinupy.algebra.tensor import m_A_x
from sinupy.mediums.plasma import relative_dielectric_tensor
plasma = mediums.ColdMagnetizedPlasma()
wave = ElectroMagneticWave()

from sympy import Eq as _Eq
from sympy import tensorcontraction as _tcontract
from sympy import tensorproduct as _tprod
m_dot_v = lambda a,b : _tcontract(_tprod(a, b), (1,2))

m_vk_x = m_A_x(wave.k)
wave_eq = waves.EM.WaveEq(plasma)
wave_eq.coeff_matrix()