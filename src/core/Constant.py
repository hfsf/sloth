"""
Define constant class.
"""

from Unit import UnitContainingObject as UCO
import numpy as np


class Constant(UCO):

    """

    Constant(Urameter class definition, that holds capabilities for:
    - Constant(Urameter definition, including its units for posterior dimensional coherence analysis
    - Constant(Urameter operations using overloaded mathematical operators, making possible an almost-writing-syntax (eg: a() + b() )

    * TODO: - Overload mathematical operators (call, add, subtract, multiply, divide) with dimensional analysis coherence    

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
