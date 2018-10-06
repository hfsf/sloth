"""
Define parameter class.
"""

import numpy as np
import Unit


class Parameter:

    """

    Parameter class definition, that holds capabilities for:
    - Parameter definition, including its units for posterior dimensional coherence analysis
    - Parameter operations using overloaded mathematical operators, making possible an almost-writing-syntax (eg: a() + b() )

    * TODO: - Overload mathematical operators (call, add, subtract, multiply, divide) with dimensional analysis coherence    

    """


    def __init__(self, name, units , description):

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
