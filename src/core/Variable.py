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
            - Provide the mathematical complex functions (abs, exp, log, log10, etc)
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
        Return the __code__ expression for ulterior evaluation of the final expression inside an equation.

        """

        return(self.value)

    def _returnProtoVariable(self, name="", units={""}, description = "", isLowerBounded = False, isUpperBounded = False, lowerBound = None, upperBound = None, value = 0):

        """
        
        Return a Variable class with given name, description and other variables (defaults to "", False and None, when aplicable). Used for return of an Variable object as the result of variable operations, with dimension given by units.

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

        return( self.__class__(name, units, description, isLowerBounded, isUpperBounded, lowerBound , upperBound, value) )

    def __add__(self, other_var):

        """

        Overloaded function for summation of two variables or one variable and one parameter, or one variable and one constant.
        The __add__ function calls self.units._checkDimensionalCoherence which uses objects
        'dimensions'. Also, uses object 'value'. Thus, parameters and constants must have this objects as their instances when summed.

        :param Variable other_var:
        Second Variable object to perform arithmetic operation.

        :rtype Variable new_var:
        Proto-variable returned as the result of the arithmetical operation

        """

        if self.units._checkDimensionalCoherence(other_var.units) == True:

            # Dimensional coherence confirmed. Insert here commands

            new_var = self._returnProtoVariable(units = self.units, value = self.value+other_var.value)

            return(new_var) 

        else:

            raise(Errors.DimensionalCoherenceError(self.units, other_var.units))

    def __sub__(self, other_var):

        """

        Overloaded function for subtraction of two variables or one variable and one parameter, or one variable and one constant.
        The __sub__ function calls self.units._checkDimensionalCoherence which uses objects
        'dimensions'. Also, uses object 'value'. Thus, parameters and constants must have this objects as their instances when subtracted.

        :param Variable other_var:
        Second Variable object to perform arithmetic operation.

        :rtype Variable new_var:
        Proto-variable returned as the result of the arithmetical operation

        """

        if self.units._checkDimensionalCoherence(other_var.units) == True:

            # Dimensional coherence confirmed. Insert here commands

            new_var = self._returnProtoVariable(units = self.units, value = self.value+other_var.value)

            return(new_var) 

        else:

            raise(Errors.DimensionalCoherenceError(self.units, other_var.units))

    def __mul__(self, other_var):

        """

        Overloaded function for multiplication of two variables or one variable and one parameter, or one variable and one constant.
        The __mul__ function does not requires dimensional coherence, but resultant variable units should be modified

        :param Variable other_var:
        Second Variable object to perform arithmetic operation.

        :rtype Variable new_var:
        Proto-variable returned as the result of the arithmetical operation

        """

        new_var = self._returnProtoVariable(units = self.units*other_var.units, value = self.value*other_var.value)

        return(new_var) 


    def __div__(self, other_var):

        """

        Overloaded function for division of two variables or one variable and one parameter, or one variable and one constant.
        The __div__ function does not requires dimensional coherence, but resultant variable units should be modified

        :param Variable other_var:
        Second Variable object to perform arithmetic operation.

        :rtype Variable new_var:
        Proto-variable returned as the result of the arithmetical operation

        """

        new_var = self._returnProtoVariable(units = self.units/other_var.units, value = self.value/other_var.value)

        return(new_var) 

    def __pow__(self, power):

        """

        Overloaded function for exponentiation of one variable or one parameter, or one constant.
        The __pow__ function does not requires dimensional coherence, but resultant variable units should be modified

        :param float power:
        Power for operation with the unit(self).

        :rtype Variable new_var:
        Proto-variable returned as the result of the arithmetical operation

        """

        new_var = self._returnProtoVariable(units = self.units**power, value = self.value**power)

        return(new_var) 