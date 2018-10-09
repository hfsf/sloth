"""
Defines overloaded operators for basic mathematical operations over unit-containing members (Constant, Parameter, Variables)
"""

class DimensionalCoherenceError(Exception):

    """
    Error raised when two non-coherent dimensions are summed
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
   