"""
Define variable class.
"""

import numpy as np
import Unit
import Error_definitions as Errors

class Variable:

    """

    Variable class definition, that holds capabilities for:
    - Variable definition, including its units for posterior dimensional coherence analysis
    - Variable operations using overloaded mathematical operators, making possible an almost-writing-syntax (eg: a() + b() )

    * TODO: - Overload mathematical operators (call, add, subtract, multiply, divide) with dimensional analysis coherence
            - Include restrictions for variable value.    

    """

    def __init__(self, name, units , description = "", isLowerBounded = False, isUpperBounded = False, lowerBound = None, upperBound = None, value = 0):

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

        self.name = name

        self.units = units

        self.description = description

        self.isLowerBounded = ( lowerBound != None ) 

        self.isUpperBounded = ( upperBound != None )

        self.lowerBound = lowerBound

        self.upperBound = upperBound

        self.value = value

    def __call__(self):

        """

        Overloaded function for calling the variable as an function. 
        Return the value stored for the variable.

        """

        return(self.value)

    def __add__(self, other_var):

        """

        Overloaded function for summation of two variables or one variable and one parameter, or one variable and one constant.
        The __add__ function calls overloaded_Operations._addUnitContainingMembers which uses objects
        'dimensions'

        :param Variable other_var:
        Second Variable object to perform arithmetic operation.

        """

        if oop._addUnitContainingMembers(self, other_var) == True:

            # Dimensional coherence confirmed. Insert here commands

            pass 

        else:

            raise(oop.DimensionalCoherenceError(self, other_var))

    def __sub__(self, other_var):

        """

        Overloaded function for subtraction of two variables or one variable and one parameter, or one variable and one constant.
        The __sub__ function calls overloaded_Operations._addUnitContainingMembers which uses objects
        'dimensions'

        :param Variable other_var:
        Second Variable object to perform arithmetic operation.

        """

        if oop._addUnitContainingMembers(self, other_var) == True:

            # Dimensional coherence confirmed. Insert here commands

            pass 

        else:

            raise(oop.DimensionalCoherenceError(self, other_var))

    def __mul__(self, other_var):

        """

        Overloaded function for multiplication of two variables or one variable and one parameter, or one variable and one constant.
        The __mul__ function does not requires dimensional coherence, but resultant variable units should be modified

        :param Variable other_var:
        Second Variable object to perform arithmetic operation.

        """

        pass

        