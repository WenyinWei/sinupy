"""Algebra utilities involved in the deduction procedure of fusion plasma physics formula.

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

################################################################################
# Judge whether a term could be a sqrted term, squared term or an absoluted term.
################################################################################

def is_sqrt(expr):
    from sympy.core.power import Pow
    from sympy.core.mul import Mul
    from sympy.core.numbers import Half
    
    is_sqrt_ = False # defaults to be False
    expr = expr.factor()
    # recurse the function on each arg if the top function is a multiplication 
    # e.g. 4 * sqrt(b) * sqrt(c) should also be regarded as a sqrt expression.
    if expr.func == Mul: 
        args_is_sqrt = [is_sqrt(arg) for arg in expr.args]
        return True if all(args_is_sqrt) else False
    # Main Function 
    elif expr.func == Pow: 
        if isinstance(expr.args[1], Half): # The second arg of Pow is a Half number if the term is a sqrt
            is_sqrt_ = True
    elif not expr.is_negative:
        is_sqrt_ = True
    return is_sqrt_

def is_square(expr):
    from sympy.core.power import Pow
    from sympy.core.mul import Mul
    
    is_square_ = False # defaults to be False
    expr = expr.factor()
    # recurse the function on each arg if the top function is a multiplication 
    # e.g. 4 * b^4 * b^6 * c^2 should also be regarded as a square expression.
    if expr.func == Mul: 
        args_is_square = [is_square(arg) for arg in expr.args]
        return True if all(args_is_square) else False
    # Main Function 
    elif expr.func == Pow:
        base, exponent = expr.args
        if exponent % 2 == 0: # The second arg of Pow is an even number if the term is a square
            is_square_ = True
    elif not expr.is_negative:
        is_square_ = True
    return is_square_

def is_abs(expr):
    from sympy.core.mul import Mul
    from sympy import Abs
    
    is_abs_ = False # defaults to be False
    expr = expr.factor()
    # recurse the function on each arg if the top function is a multiplication 
    # e.g. 4 * Abs(b) * Abs(c) should also be regarded as a abs expression.
    if expr.func == Mul: 
        args_is_abs = [is_abs(arg) for arg in expr.args]
        return True if all(args_is_abs) else False
    # Main Function 
    elif expr.func == Abs: 
        is_abs_ = True
    elif not expr.is_negative:
        is_abs_ = True 
    return is_abs_

def signed_sqrt(expr):
    """Signed sqrt operator

    Args:
        expr (sympy.expr): sympy expression

    Returns:
        sympy.expr: A simplified expression
    """
    from functools import reduce
    from sympy.core.power import Pow
    from sympy.core.mul import Mul
    from sympy import sqrt

    expr = expr.factor()
    # recurse the function on each arg if the top function is a multiplication 
    # e.g. signed_sqrt( 4 * b^2 ) == 2 * b 
    if expr.func == Mul: 
        args_signed_sqrt = [signed_sqrt(arg) for arg in expr.args]
        return reduce(Mul, args_signed_sqrt)
    elif expr.func == Pow:
        base, exponent = expr.args
        if exponent.is_even:
            return base**(exponent/2)
    return sqrt(expr)
        
def are_quadratic_sols(expr1, expr2):
    # Suppose the function is a form of -b +/- sqrt(Delta) / 2a, where Delta = b^2 - 4ac
    
    expr_sum  = expr1 + expr2 # -b/a
    expr_diff = expr1 - expr2 # +/- sqrt(Delta)/a
    expr_prod = expr1 * expr2 # c/a
    # b^2/a^2 - 4 c/a == (b^2 - 4ac) / a^2 
    lhs = (expr_sum ** 2 - 4 * expr_prod).simplify()
    rhs = (expr_diff ** 2).simplify()
    lhs_minus_rhs = (lhs - rhs).simplify()
    return True if lhs_minus_rhs==0 else False

def simplify_quadratic_sols(expr1, expr2):
    if not are_quadratic_sols(expr1, expr2):
        raise ValueError("The input expr1, expr2 may not be a pair of solutions of a quadratic equation. Make sure they look like -b +/- sqrt(Delta) / 2a.")

    expr_sum  =(expr1 + expr2).simplify() # -b/a
    expr_diff =(expr1 - expr2).simplify() # +/- sqrt(Delta)/a
    
    signed_sqrt_Delta_on_a = signed_sqrt(expr_diff**2) # Still +/- sqrt(Delta)/a, but simplified
    
    simplified_expr1 = (expr_sum + signed_sqrt_Delta_on_a)/2
    simplified_expr2 = (expr_sum - signed_sqrt_Delta_on_a)/2
    simplified_expr1 = simplified_expr1.simplify()
    simplified_expr2 = simplified_expr2.simplify()
    return simplified_expr1, simplified_expr2

