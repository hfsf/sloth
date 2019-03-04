# *coding:utf-8*

"""
Define the Quantity (QTY), base-class for all unit-containg objects (Variables, Parameters, Constants)
"""

import copy
from .error_definitions import DimensionalCoherenceError, UnexpectedValueError
import sympy as sp
from .expression_evaluation import EquationNode

# Null dimension dict
null_dimension = {'m':0.0,'kg':0.0,'s':0.0,'A':0.0,'K':0.0,'mol':0.0,'cd':0.0}

class Quantity:  # New-style class syntax

    """
    Return an Quantity (QTY) class with given name, description and other variables
    (defaults to "", False and None, when aplicable). Used for return of an Variable object as the result of variable operations, with dimension given by units

    :ivar str name:
    Name for the current QTY

    :ivar Unit units:
    Definition of dimensional unit of current QTY

    :ivar str description:
    Description for the present QTY. Defauls to ""

    * TODO: Ensure that 'value' is a float for minimization of round-off errors

    """

    def __init__(self, name, units, description="", value=0., latex_text=""):
        """
        Instantiate Quantity.

        :ivar str name:
            Name for the current Quantity (QTY)

        :ivar Unit units:
            Definition of dimensional unit of current QTY

        :ivar str description:
            Description for the present QTY. Defaults to ""

        :ivar float value:
            Value of the current QTY. Defaults to 0.

        :ivar str latex_text:
            Text for latex representation
        """

        self.name = name

        self.units = units

        self.description = description

        self.value = value

        self.latex_text = latex_text

        self.is_specified = False


    def setValue(self, quantity_value, quantity_unit=None):

        """
        Set the current value for the Quantity object given a value and optionally an Unit object
        """
        if isinstance(quantity_value, self.__class__):


            if quantity_unit == None and  quantity_value.units._check_dimensional_coherence(self.units) == True:

                self.value = quantity_value.value

                self.is_specified = True

            else:

                raise DimensionalCoherenceError(self.units,quantity_value.units)

        elif isinstance(quantity_value, float) or isinstance(quantity_value, int) and quantity_unit==None:

            self.value = quantity_value

            self.is_specified = True

        elif isinstance(quantity_value, float) or isinstance(quantity_value, int) and quantity_unit!=None and quantity_unit._check_dimensional_coherence(self.units):

            self.value = quantity_value

            self.is_specified = True

        else:

            raise UnexpectedValueError("(Quantity, float, int)")

    def __call__(self):
        """
        Overloaded function for calling the QTY as an function. 
        Return an EquationNode object.

        :return:
            Return an EquationNode object corresponding to current QTY object
        :rtype EquationNode:
        """

        # If the object is not specified (eg:var)

        if self.is_specified == False:

            return EquationNode(name=self.name, 
                                symbolic_object=sp.symbols(self.name), 
                                symbolic_map={self.name:self},
                                variable_map={self.name:self}, 
                                unit_object=self.units,
                                latex_text=self.latex_text,
                                repr_symbolic=sp.symbols(self.name)
                                )

        # If the object is specified (eg:specified param)

        if self.is_specified == True:

            return EquationNode(name=self.name, 
                                symbolic_object=self.value, 
                                symbolic_map={self.name:self},
                                variable_map={}, 
                                unit_object=self.units,
                                latex_text=self.latex_text,
                                repr_symbolic=sp.symbols(self.name)
                                )

    def __add__(self, other_obj):
        """
        Overloaded function for summation of two unit-containing-objects.
        The __add__ function calls self.units._check_dimensional_coherence which uses objects
        'dimensions'. Also, uses object 'value'. Thus, parameters and constants must have this objects as their instances when summed.

        :param Variable other_obj:
        Second Variable object to perform arithmetic operation.

        :rtype Variable new_obj:
        Proto-variable returned as the result of the arithmetical operation
        """

        if self.units._check_dimensional_coherence(other_obj.units) == True:

            # Dimensional coherence confirmed. Insert here commands

            new_obj = self.__class__(units = self.units, value = self.value+other_obj.value)

            return new_obj

        else:

            raise(DimensionalCoherenceError(self.units, other_obj.units))

    def __sub__(self, other_obj):
        """
        Overloaded function for subtraction of two unit-containing-objects.
        The __sub__ function calls self.units._check_dimensional_coherence which uses objects
        'dimensions'. Also, uses object 'value'. Thus, parameters and constants
        must have this objects as their instances when subtracted.

        :param Variable other_obj:
            Second Variable object to perform arithmetic operation.

        :return:
            Proto-variable returned as the result of the arithmetical operation
        :rtype Variable new_obj
        """

        if self.units._check_dimensional_coherence(other_obj.units) == True:

            # Dimensional coherence confirmed. Insert here commands

            new_obj = self.__class__(units = self.units, value = self.value-other_obj.value)

            return new_obj

        else:

            raise(DimensionalCoherenceError(self.units, other_obj.units))

    def __mul__(self, other_obj):
        """
        Overloaded function for multiplication of two unit-containing-objects.
        The __mul__ function does not requires dimensional coherence, 
        but resultant variable units should be modified.

        :param Variable other_obj:
            Second Variable object to perform arithmetic operation.

        :return:
            Proto-variable returned as the result of the arithmetical operation
        :rtype Variable new_obj:
        """

        new_obj = self.__class__(units = self.units*other_obj.units, value = self.value*other_obj.value)

        return new_obj

    def __div__(self, other_obj):
        """
        Overloaded function for division of two unit-containing-objects.
        The __div__ function does not requires dimensional coherence, 
        but resultant variable units should be modified.

        :param Variable other_obj:
            Second Variable object to perform arithmetic operation.

        :return:
            Proto-variable returned as the result of the arithmetical operation
        :rtype Variable new_obj:
        """

        new_obj = self.__class__(units = self.units/other_obj.units, value = self.value/other_obj.value)

        return(new_obj) 

    def __pow__(self, power):

        """

        Overloaded function for exponentiation of one unit-containing-object.
        The __pow__ function does not requires dimensional coherence, but resultant variable units should be modified

        :param float power:
        Power for operation with the unit(self).

        :rtype Variable new_obj:
        Proto-variable returned as the result of the arithmetical operation

        """

        new_obj = self.__class__( units = self.units**power.value, value = self.value**power.value )

        return(new_obj) 
