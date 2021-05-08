"""Algebra utilities involved in the deduction procedure of fusion plasma physics formula.

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

def find_singularities(expr, var):
    from sympy.core.power import Pow
    from sympy.core.mul import Mul
    from sympy.core.add import Add
    from sympy import solve, Eq
    from operator import or_
    from functools import reduce

    # recurse the function on each arg if the top function is an addition
    # e.g. 4 * sqrt(b) * sqrt(c) should also be regarded as a sqrt expression.
    if expr.func == Add or expr.func == Mul:
        args_singularities_ = [find_singularities(arg, var) for arg in expr.args]
        return reduce(or_, args_singularities_) # This trick from Alexander Klimenko, https://stackoverflow.com/questions/17429123/how-to-join-two-sets-in-one-line-without-using
    # Main Function 
    elif expr.func == Pow and expr.args[1].is_negative: # The second arg of Pow is a negative number if the term is a denominator
        return set(solve( Eq(expr.args[0], 0), var )) | find_singularities(expr.args[0], var)
    else:
        return set()


# def find_singularities_with_type(expr, var, n_or_d, part_of_addition:bool):
#     from sympy.core.power import Pow
#     from sympy.core.mul import Mul
#     from sympy.core.add import Add
#     from sympy import solve, Eq
#     from operator import or_
#     from functools import reduce

#     # recurse the function on each arg if the top function is an addition
#     # e.g. 4 * sqrt(b) * sqrt(c) should also be regarded as a sqrt expression.
#     if expr.func == Add:
#         args_singularities_ = [find_singularities_with_type(arg, var, n_or_d, part_of_addition=True) for arg in expr.args]
#         return reduce(or_, args_singularities_) # This trick from Alexander Klimenko, https://stackoverflow.com/questions/17429123/how-to-join-two-sets-in-one-line-without-using
#     if expr.func == Mul:
#         args_singularities_ = [find_singularities_with_type(arg, var, n_or_d, part_of_addition=False) for arg in expr.args]
#         return reduce(or_, args_singularities_) # This trick from Alexander Klimenko, https://stackoverflow.com/questions/17429123/how-to-join-two-sets-in-one-line-without-using
#     # Main Function 
#     elif expr.func == Pow and expr.args[1].is_negative: # The second arg of Pow is a negative number if the term is a denominator
#         if n_or_d == 'n':
#             singularities_ = [(sol, 'inf') for sol in solve( Eq(expr.args[0], 0), var )]
#         elif n_or_d == 'd' and not part_of_addition:
#             singularities_ = [(sol, 'zero') for sol in solve( Eq(expr.args[0], 0), var )]
#         elif n_or_d
#         return set(singularities_) | find_singularities_with_type(expr.args[0], var, not n_or_d)
#     else:
#         return set()

def find_zeroes(expr, var):
    """find all zero points of a sympy expression(var).

    Args:
        expr (sympy.expr): The sympy expression for which the zero points are requested.
        var (sympy.expr): The variable(s) of the expression

    Returns:
        set: a set of floating numbers which are the variable values as the zero points of the expression.

    Note:
        The most naive way to find zeros is to use sympy.solve(sympy.Eq(expr, 0), var). 
        However, if we use the following expr as an example,
        (1/(x-2)+2) / (1 + 1/x + 1/(x-1))
        sympy.solve can only find the x=3/2 zero point, without the x=0 and x=1. 

        Our custom function is more smart, it can find more complete solutions, {0,1,3/2} in the above example.
        I admit that this find_zeroes function has not been comprehensive due to its simple implementation, yet smart enough for the code author's application. 
        
    """
    from sympy.core.power import Pow
    from sympy.core.mul import Mul
    from sympy.core.add import Add
    from sympy import solve, Eq, cancel, fraction
    from operator import or_
    from functools import reduce

    # recurse the function on each arg if the top function is an addition
    # e.g. 4 * sqrt(b) * sqrt(c) should also be regarded as a sqrt expression.
    expr = cancel(expr)
    n, d = fraction(expr)
    zeros_from_numerator = set(solve( Eq(n, 0), var ))
    return zeros_from_numerator


def split_logspace(start, stop, breakpoints:set, num=50, 
                   endpoint=True , base=10.0, dtype=None):
    from numpy import logspace
    start_end_pair = sorted({point for point in breakpoints if point > start and point < stop})
    start_end_pair = [start] + start_end_pair + [stop]
    result = []
    for i in range(len(start_end_pair)-1):
        subnum = int( (start_end_pair[i+1] - start_end_pair[i]) * num / (stop - start) )
        if endpoint:
            result.append(
                logspace(start_end_pair[i], start_end_pair[i+1], subnum, endpoint, base, dtype)
            )
        else:
            subspacing = (start_end_pair[i+1] - start_end_pair[i]) / subnum
            result.append(
                logspace(start_end_pair[i] + subspacing, start_end_pair[i+1], subnum, endpoint, base, dtype)
            )
    return result

    