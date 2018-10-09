"""
Defines overloaded operators for basic mathematical operations over unit-containing members (Constant, Parameter, Variables)
"""
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
   