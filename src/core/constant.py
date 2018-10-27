"""
Define constant class.
"""

from quantity import Quantity
from unit import null_dimension


def convert_to_constant(num):
    """
    Convert one float argument to Constant, returning the converted object.

    :param float num:
        Float number to be converted to Constant

    :return:
        Float number converted to a Constant object
    :rtype: object
    """

    return Constant(name=str(num), units = null_dimension, value = float(num) )


class Constant(Quantity):
    """
    Constant class definition, that holds capabilities for:

    * Constant definition, including its units for posterior dimensional coherence analysis

    * Constant operations using overloaded mathematical operators,
    making possible an almost-writing-syntax (eg: a() + b() )
    """

    def __init__(self, name, units , description="", value=0, latex_text=""):

        super().__init__(name, units, description, value, latex_text)

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
