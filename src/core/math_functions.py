"""
Define mathematical functions designed to work with unit-containing variables, such as Variables, Parameters, etc.

By default, all those functions perform a sanity check in the dimensions of the UCO argument and raise an
NonDimensionalArgument error. This can be avoided with the argument ignore_dimensions = True.
"""

from numpy import log, log10, exp, abs, sin, cos, tan
import copy
import Error_definitions as Errors
import Unit

dimless_ = Unit.Unit("dimless", Unit.null_dimension, "a generic dimensionless unit")

def Log(obj, ignore_dimensions=False):

    """
    Computes the natural logarithm (neper) of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if dimless_._checkDimensionalCoherence(obj.units) == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = np.log(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = np.log(obj.value)

    return(res)


def Log10(obj, ignore_dimensions=False):

    """
    Computes the logarithm of base-10 of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if dimless_._checkDimensionalCoherence(obj.units) == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = np.log10(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = np.log10(obj.value)

    return(res)


def Exp(obj, ignore_dimensions=False):

    """
    Computes the exponential function of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if dimless_._checkDimensionalCoherence(obj.units) == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = np.exp(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = np.exp(obj.value)

    return(res)


def Abs(obj, ignore_dimensions=False):

    """
    Computes the absolute value of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if dimless_._checkDimensionalCoherence(obj.units) == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = np.abs(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = np.abs(obj.value)

    return(res)


def Sin(obj, ignore_dimensions=False):

    """
    Computes the sin value of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if dimless_._checkDimensionalCoherence(obj.units) == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = np.sin(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = np.sin(obj.value)

    return(res)


def Cos(obj, ignore_dimensions=False):

    """
    Computes the cosin value of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if dimless_._checkDimensionalCoherence(obj.units) == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = np.cos(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = np.cos(obj.value)

    return(res)


def Tan(obj, ignore_dimensions=False):

    """
    Computes the tangent of an Quantity.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Quantity

    :rtype Object-like res:
    Resultant object, with the same type as the input argument.

    """

    if ignore_dimensions != True:

        if dimless_._checkDimensionalCoherence(obj.units) == True:

            # Dimensional coherence confirmed. Insert here commands

            res = copy(obj)

            res.value = np.tan(obj.value)

        else:

            raise(Errors.NonDimensionalArgumentError(obj.units))

    else:

        res = copy(obj)

        res.value = np.tan(obj.value)

    return(res)