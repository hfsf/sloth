"""
Define variable class.
"""

from .quantity import Quantity

class Variable(Quantity):

    """

    Variable class definition, that holds capabilities for:
    - Variable definition, including its units for posterior dimensional coherence analysis
    - Variable operations using overloaded mathematical operators, making possible an almost-writing-syntax (eg: a() + b() )

    """

    def __init__(self, name, units , description = "", is_lower_bounded = False, is_upper_bounded = False, lower_bound = None, upper_bound = None,  value = 0, latex_text=""):

        super().__init__(name, units, description, value, latex_text)

        """
        Initial definition.

        :param str name:
        Name for the current variable

        :param Unit units:
        Definition of dimensional unit of current variable

        :param str description:
        Description for the present variable. Defauls to ""

        :param bool isLower_bounded:
        Define if the Variable object has some minimum value restriction.
        A sanity check is performed and if lowerBound != None, isLowerBounded = True.

        :param bool isUpper_bounded:
        Define if the Variable object has some maximum value restriction.
        A sanity check is performed and if upperBound != None, isUpperBounded = True.

        :param float lower_bound:
        Minimum value for Variable object

        :param float upper_bound:
        Minimum value for Variable object

        :param float value:
        Value of the current variable. Defaults to 0.       

        === Coming from base class ===

        self.name = name

        self.units = units

        self.description = description

        self.value = value

        """

        self.is_lower_bounded = ( lower_bound != None ) 

        self.is_upper_bounded = ( upper_bound != None )

        self.lower_bound = lower_bound

        self.upper_bound = upper_bound

