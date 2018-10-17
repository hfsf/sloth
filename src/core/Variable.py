"""
Define variable class.
"""

from Unit import Quantity
import Error_definitions as Errors

class Variable(Quantity):

    """

    Variable class definition, that holds capabilities for:
    - Variable definition, including its units for posterior dimensional coherence analysis
    - Variable operations using overloaded mathematical operators, making possible an almost-writing-syntax (eg: a() + b() )

    * TODO: - Overload mathematical operators (call, add, subtract, multiply, divide) with dimensional analysis coherence
            - Provide the mathematical complex functions (abs, exp, log, log10, etc)
            - Include restrictions for variable value.    

    """

    def __init__(self, name, units , description = "", isLowerBounded = False, isUpperBounded = False, lowerBound = None, upperBound = None, value = 0):

        super(self.__class__,self).__init__(name, units, description, value)

        """
        Initial definition.

        :param str name:
        Name for the current variable

        :param Unit units:
        Definition of dimensional unit of current variable

        :param str description:
        Description for the present variable. Defauls to ""

        :param bool isLowerBounded:
        Define if the Variable object has some minimum value restriction.
        A sanity check is performed and if lowerBound != None, isLowerBounded = True.

        :param bool isUpperBounded:
        Define if the Variable object has some maximum value restriction.
        A sanity check is performed and if upperBound != None, isUpperBounded = True.

        :param float lowerBound:
        Minimum value for Variable object

        :param float upperBound:
        Minimum value for Variable object

        :param float value:
        Value of the current variable. Defaults to 0.       

        """

        """

        === Coming from base class ===

        self.name = name

        self.units = units

        self.description = description

        self.value = value

        """

        self.isLowerBounded = ( lowerBound != None ) 

        self.isUpperBounded = ( upperBound != None )

        self.lowerBound = lowerBound

        self.upperBound = upperBound

