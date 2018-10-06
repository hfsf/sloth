"""
Define variable class.
"""

import numpy as np
import Unit


class Variable:

    """

    Variable class definition, that holds capabilities for:
    - Variable definition, including its units for posterior dimensional coherence analysis
    - Variable operations using overloaded mathematical operators, making possible an almost-writing-syntax (eg: a() + b() )

    * TODO: - Overload mathematical operators (call, add, subtract, multiply, divide) with dimensional analysis coherence
            - Include restrictions for variable value.    

    """


    def __init__(self, name, units , description = "", isBounded = False, lowerBound = None, upperBound = None):

        """
        Initial definition.

        :param str name:
        Name for the current variable

        :param Unit units:
        Definition of dimensional unit of current variable

        :param str description:
        Description for the present variable. Defauls to ""

        """

        self.name = name

        self.units = units

        self.description = description
