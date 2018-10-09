"""
Define mathematical functions designed to work with unit-containing variables, such as Variables, Parameters, etc.
"""

import numpy as np
import copy


def log(obj):

    """
    Computes the natural logarithm (neper) of an unit-containing object.

    :param [Variable, Parameter, Constant] obj:
    Unit-containing object

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    res = copy(obj)

    res.value = np.log(obj.value)

    return(res)