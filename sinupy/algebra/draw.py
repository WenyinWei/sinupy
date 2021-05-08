"""Convenient draw utilities for sympy expression.

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

def draw_discontinuable_expr(exprs, var, varlim, exprlim=None, var_is_yaxis=False, num=50, var_sample_scale='linear', fig=None, ax=None, labels=None, list_subkwarg=None):
    from numpy import linspace, logspace, logical_or, log10, nan
    from sympy import lambdify
    
    if ax is None:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        
    for i, expr in enumerate(exprs):
        if var_sample_scale == 'linear':
            range_ = linspace(varlim[0], varlim[1], num=num)
        elif var_sample_scale == 'log':
            range_ = logspace(log10(varlim[0]), log10(varlim[1]), num=num)
        else:
            raise ValueError("Choose either linear or log scale.")
        
        values_ = lambdify(var, expr, 'numpy')(range_)
        if exprlim:
            if exprlim[0]:
                values_[values_ < exprlim[0]] = nan
            if exprlim[1]:
                values_[values_ > exprlim[1]] = nan

        if not var_is_yaxis:
            plot_func_args = (range_, values_)
        else:
            plot_func_args = (values_, range_)

        if list_subkwarg and list_subkwarg[i]:
            plot_func_kwargs = list_subkwarg[i]
        else: 
            plot_func_kwargs = dict()
        if labels is not None: 
            plot_func_kwargs['label'] = labels[i]

        ax.plot(*plot_func_args, **plot_func_kwargs)
        
    return fig, ax

def add_line_with_slope(ax, k:float, num=50, **kwargs):
    from numpy import linspace
    lower, upper = ax.get_xbound()
    x_range_ = linspace(lower, upper, num=num)
    y_range_ = k * x_range_ 
    ax.plot(x_range_, y_range_, **kwargs)