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

def log(obj, ignore_dimensions=False):

    """
    Computes the natural logarithm (neper) of an unit-containing object.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Unit-containing object

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


def log10(obj, ignore_dimensions=False):

    """
    Computes the logarithm of base-10 of an unit-containing object.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Unit-containing object

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


def exp(obj, ignore_dimensions=False):

    """
    Computes the exponential function of an unit-containing object.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Unit-containing object

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


def abs(obj, ignore_dimensions=False):

    """
    Computes the absolute value of an unit-containing object.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Unit-containing object

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


def sin(obj, ignore_dimensions=False):

    """
    Computes the sin value of an unit-containing object.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Unit-containing object

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


def cos(obj, ignore_dimensions=False):

    """
    Computes the cosin value of an unit-containing object.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Unit-containing object

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


def tan(obj, ignore_dimensions=False):

    """
    Computes the tangent of an unit-containing object.
    The function uses objects 'dimensions' and 'value' from obj.
    By default, If ignore_dimensions
    THe value is calculated using np.log

    :param [Variable, Parameter, Constant] obj:
    Unit-containing object

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