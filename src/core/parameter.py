"""
Define parameter class.
"""

from unit import Quantity
import numpy as np


class Parameter(Quantity):

    """

    Parameter class definition, that holds capabilities for:
    - Parameter definition, including its units for posterior dimensional coherence analysis
    - Parameter operations using overloaded mathematical operators, making possible an almost-writing-syntax (eg: a() + b() )

    """


    def __init__(self, name, units , description="", value=0, latex_text=""):

        super(self.__class__,self).__init__(name, units, description, value, latex_text)

        """
        Initial definition.

        :param str name:
        Name for the current parameter

        :param Unit units:
        Definition of dimensional unit of current parameter

        :param str description:
        Description for the present parameter. Defauls to ""

        """

        self.name = name

        self.units = units

        self.description = description
