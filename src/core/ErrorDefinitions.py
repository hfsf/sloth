"""
Defines overloaded operators for basic mathematical operations over unit-containing members (Constant, Parameter, Variables)
"""

class UnexpectedValueError(Exception):

    """
    Error raised by input of an unexpected value. Typically, when the user should input a string an insert a numerical value.
    """

    def __init__(self, expected_type):

        self.expected_type = expected_type

    def __str__(self):

        msg = "Unexpected value error. A %s was expected, but one divergent type was supplied." % (self.expected_type)

        return(msg)


class UnresolvedPanicError(Exception):

    """
    Error raised by unresolved problems. Ideally this exception would never arises. It is included only for debugging purposes
    """

    def __init__(self):

        pass

    def __str__(self):

        msg = "Unresolved Panic Error. This should not have ocurrred. \n Perhaps you should debug your code."

        return(msg)



class NonDimensionalArgumentError(Exception):

    """
    Error raised when a non-dimensional argument was expected but a dimensional one was provided.
    Typically occurs in transcendental functions (log, log10, sin, cos, etc...)
    """

    def __init__(self, unit):

        self.unit = unit

    def __str__(self):

        msg = "A dimensionless argument was expected \n" + \
              str(self.unit.dimension)

        return(msg)

class DimensionalCoherenceError(Exception):

    """
    Error raised when two non-coherent dimensions are summed or subtracted
    """
    def __init__(self, unit_1, unit_2):

        self.unit_1 = unit_1

        self.unit_2 = unit_2

    def __str__(self):

        msg = "Dimensions are incohent \n(" + \
               str(self.unit_1.dimension)   + \
               "\n != \n"                       + \
               str(self.unit_2.dimension)   + \
               ")."

        return(msg)


def _addUnitContainingOperations(a,b):

    return(a._checkDimensionalCoherence(b))
   