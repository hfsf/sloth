"""
Define mathematical functions designed to work with unit-containing variables, such as Variables, Parameters, etc.

By default, all those functions perform a sanity check in the dimensions of the UCO argument and raise an
NonDimensionalArgument error. This can be avoided with the argument ignore_dimensions = True.
"""

from numpy import log, log10, exp, abs, sin, cos, tan
from copy import copy
import ErrorDefinitions as Errors
import Unit

def Log(obj, ignore_dimensions=False):

    """
    Computes the natural logarithm (neper) of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if obj.units._isDimless_() == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = log(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = log(obj.value)

    return(res)


def Log10(obj, ignore_dimensions=False):

    """
    Computes the logarithm of base-10 of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if obj.units._isDimless_() == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = log10(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = log10(obj.value)

    return(res)


def Exp(obj, ignore_dimensions=False):

    """
    Computes the exponential function of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if obj.units._isDimless_() == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = exp(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = exp(obj.value)

    return(res)


def Abs(obj, ignore_dimensions=False):

    """
    Computes the absolute value of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if obj.units._isDimless_() == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = abs(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = abs(obj.value)

    return(res)


def Sin(obj, ignore_dimensions=False):

    """
    Computes the sin value of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if obj.units._isDimless_() == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = sin(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = sin(obj.value)

    return(res)


def Cos(obj, ignore_dimensions=False):

    """
    Computes the cosin value of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if obj.units._isDimless_() == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = cos(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = cos(obj.value)

    return(res)


def Tan(obj, ignore_dimensions=False):

    """
    Computes the tangent of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if obj.units._isDimless_() == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = tan(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = tan(obj.value)

    return(res)