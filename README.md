# The sinupy Package

The `sinupy` package makes it convenient to analyze the characteristic sinusoidal waves propagating in various kinds of medium. Typical waves in plasma have been given in the code to demonstrate how the package works and other users are free to follow the steps to research on their medium or charcteristic waves of interest.
## Wave Equation

The electromagnetic wave equation is the theoretical basics of our formula derivation. The following formulas reveal what we call as the tensor coefficient matrix $T$

![wave_equation](https://wxy-1259064855.cos.ap-beijing.myqcloud.com/img/wave_equation_1620560123020.png)



You can acquire the `sympy.Array` representation of the above (tensor) matrix coefficients by the `WaveEq` class' `coeff_matrix()` method. For the relevant variable, you can get them by attribute *e.g.*, `wave_eq.wave.k[1]` means the wave's $k_y$ component of $\vec{k}$ vector.

## Example Snapshots

### How the refraction index $N$ changes with $\omega$ and $\theta$

![N2(omega_theta)](https://wxy-1259064855.cos.ap-beijing.myqcloud.com/img/N2(omega_theta)_1620558947574.png)

### $\omega-\vec{k}$ Diagram
![w_k](https://wxy-1259064855.cos.ap-beijing.myqcloud.com/img/w_k_1620558958144.png)

Refer to the `sinupy/nb/dispersion_relation.ipynb` for more info.
### The Famous CMA Diagram in Plasma Physics
![CMA](https://wxy-1259064855.cos.ap-beijing.myqcloud.com/img/CMA_1620558952738.png)

Refer to the `sinupy/nb/CMA.ipynb` for more info.



## Usage Tips

- Unstable APIs

    The APIs are not stable now, please contact Wenyin Wei (wenyin.wei.ww@gmail.com) for face-to-face communication to save your time. Though unstable, they are *easy to understand*, if the user is familiar with Python enough, he or she can easily recognize the techniques and tricks the package uses.

    The jupyter notebooks in the `sinupy/nb` folder are complete and self-contained to allow the newcoming users to understand how the code works.

- Consider the users of this package are scientists who spend a lot of time on the decution of physical formulas, *the attributes in any classes in sinupy are intentionally set public without leading underscores* `_`.

- Sympy Variable Name Crash

    The variable name crash is very dangerous in sinupy so we carefully choose our sympy name to avoid they happen to be the same. For example, we do not expect the computer get confused between the static magnetic field attribute `B` in `MagnetizedPlasma` and the dynamic field `B` in `ElectroMagneticWave`, of which the definitions are as:

    ```python
    # ElectroMagneticWave
    B_x, B_y, B_z = _symbols('B_x_{varidx}, B_y_{varidx}, B_z_{varidx}'.format(varidx=self.varidx), complex=True)
    self.B = _Array([B_x, B_y, B_z])
    # MagnetizedPlasma
    B_x, B_y, B_z = _symbols('B_x, B_y, B_z')
    self.B = _Array([B_x, B_y, B_z])
    ```

    For sinupy, `varidx` is a class attribute to help distinguish various physical quantities, which defaults to be a string with nothing ''. Therefore, users do not need to worry, when `varidx` defaults to be '',  about that `B_x_` crashes with `B_x`, because sympy recognize them as different symbols due to the trailing underscore `_`.

    For other variables that may coincide, users should be careful when they define their own variables. The probability to name crashes is not that big if the user defines long enough names.

- What if I really want to replace a pre-existing variable name in sinupy? 

    In most of cases, the pre-existing variable names would not cause big troubles, because the symbols would not interwine in one formula. However, when the user wants to cancel some pre-existing variables because they occupy some names that are very concise and meaningful, they can choose to inherit the class where the variable attribute is defined and override the constructor. We try to make sinupy as open as posisble to extension and the python inheritance hierarchy helps a lot. Using a custom class generally works well in sinupy.

## Goal

- Be a standard formula deduction in sinusoidal analysis.
- Extend to general curvilinear coordinate system with the help of einsteinpy.
- Multi-wave coupling relation and their respective growth rate.