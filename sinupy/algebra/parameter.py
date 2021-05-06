"""Algebra utilities involved in the deduction procedure of fusion plasma physics formula.

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

from scipy.constants import e as _e
from scipy.constants import m_e as _m_e
from scipy.constants import m_n as _m_n
from scipy.constants import m_p as _m_p
from scipy.constants import epsilon_0 as _epsilon_0
from scipy.constants import physical_constants as _physical_constants
from sympy import sqrt as _sqrt

def omega_cs(q_e, m, B):
    omega_cs_ = abs(q_e) * _e * B / m
    return omega_cs_, 'rad s^-1', None
def omega_ps(n_0, q_e, m, B):
    omega_ps_ = (q_e*_e) * _sqrt( n_0 / (_epsilon_0 * m) ) # Split the square of q_e * e, avoid it being too little
    return omega_ps_, 'rad s^-1', None

def omega_ce(B):
    return omega_cs(-1, _m_e, B)
def omega_pe(n_0, B):
    return omega_ps(n_0, -1, _m_e, B)

def omega_cp(B):
    return omega_cs(+1, _m_p, B)
def omega_pp(n_0, B):
    return omega_ps(n_0, +1, _m_p, B)

def mass_electron():
    return _physical_constants['electron mass']
def mass_proton():
    return _physical_constants['proton mass']
def mass_deuteron():
    return _physical_constants['deuteron mass']
def mass_triton():
    return _physical_constants['triton mass']

def omega_cD(B):
    m_D = _physical_constants['deuteron mass'][0]
    return omega_cs(+1, m_D, B)
def omega_pD(n_0, B):
    m_D = _physical_constants['deuteron mass'][0]
    return omega_ps(n_0, +1, m_D, B)

def omega_cT(B):
    m_T = _physical_constants['triton mass'][0]
    return omega_cs(+1, m_T, B)
def omega_pT(n_0, B):
    m_T = _physical_constants['triton mass'][0]
    return omega_ps(n_0, +1, m_T, B)