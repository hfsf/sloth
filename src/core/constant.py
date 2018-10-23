"""
Define constant class.
"""

from unit import Quantity, null_dimension
import numpy as np


def convert_to_constant(num):

    """

    Convert one float argument to Constant, returning the converted object.

    :param [float,int] num:
    Float number to be converted to Constant

    """

    return(Constant( name = str(num), units = null_dimension, value = float(num) ))

class Constant(Quantity):

    """

    Constant class definition, that holds capabilities for:
    - Constant definition, including its units for posterior dimensional coherence analysis
    - Constant operations using overloaded mathematical operators, making possible an almost-writing-syntax (eg: a() + b() )

    """

    def __init__(self, name, units , description="", value=0):

        super(self.__class__,self).__init__(name, units, description, value)

        """
        Initial definition.

        :param str name:
        Name for the current constant

        :param Unit units:
        Definition of dimensional unit of current constant

        :param str description:
        Description for the present constant. Defauls to ""

        """

        self.name = name

        self.units = units

        self.description = description
