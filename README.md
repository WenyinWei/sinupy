# The sinupy Package

The sinupy package makes it convenient to analyze the characteristic sinusoidal waves propagating in various kinds of medium. Typical waves in plasma have been given in the code to demonstrate how the package works and other users are free to follow the steps to research on their medium or charcteristic waves of interest.


## Usage Tips

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