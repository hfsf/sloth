# *coding:utf-8*

"""
Define Unit class, for ulterior utilization (eg:Variable,Parameter)

Define the Quantity (QTY), base-class for all unit-containg objects (Variables, Parameters, Constants)
"""

import copy
import error_definitions as errors
from expression_evaluation import EquationNode, ExpressionTree

# Null dimension dict
null_dimension = {'m':0.0,'kg':0.0,'s':0.0,'A':0.0,'K':0.0,'mol':0.0,'cd':0.0}


class Quantity:  # New-style class syntax
    """
    Return an Quantity (QTY) class with given name, description and other variables
    (defaults to "", False and None, when aplicable). Used for return of an Variable object
    as the result of variable operations, with dimension given by units

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

    def _return_proto_object(self, name="", units={""}, description="", value=0):
        """
        Return a Proto Quantity (QTY) class with given name, description and other
        variables (defaults to "", False and None, when applicable). Used for return of an
        Variable object as the result of variable operations, with dimension given by units.

        :param name:
            Proto Quantity name

        :param units:
            Dimension of Variable object result

        :param description:
            Description of the Proto Quantity object

        :param value:
            Value attached

        :return:
            A Proto Quantity Object
        :rtype: object
        """
        return self.__class__(name=name, units=units, description=description, value=value)

    def __call__(self):
        """
        Overloaded function for calling the QTY as an function. 
        Return the EquationNode expression for composition of an ExpressionTree
        """

        return ExpressionTree(
            EquationNode(name=self.name, base_object=self, latex_text=self.latex_text)
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

            new_obj = self._return_proto_object(units = self.units, value = self.value+other_obj.value)

            return new_obj

        else:

            raise(errors.DimensionalCoherenceError(self.units, other_obj.units))

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

            new_obj = self._return_proto_object(units = self.units, value = self.value+other_obj.value)

            return new_obj

        else:

            raise(errors.DimensionalCoherenceError(self.units, other_obj.units))

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

        new_obj = self._return_proto_object(units = self.units*other_obj.units, value = self.value*other_obj.value)

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

        new_obj = self._return_proto_object(units = self.units/other_obj.units, value = self.value/other_obj.value)

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

        new_obj = self._return_proto_object(
                                          units = self.units**power.value, \
                                          value = self.value**power.value
                                         )

        return(new_obj) 


class Unit:  # New-style class syntax
    """
    Unit class definition, that holds the capabilities:
    - Dictionary containing the dimensional index for each SI dimension, 
    used in dimensional coherence analysis in proper classes (eg: Variable, Parameter)
    - Unit operations using overloaded mathematical operators 
    (multiplication, division, power), making possible an almost-writing-syntax
    """

    def __init__(self, name, dimension_dict, description=""):
        """
        Initial definition

        :param str name:
            Name of the present unit.

        :param (dict(float) or Unit) dimension_dict:
            Dictionary (ou proper unit) containing dimensions for the present unit, and corresponding indexes. Absent units are assumed 0.
            eg: {'m':1,'s':-1} -> m/s (velocity)

        :param str description:
            Description of the present unit. Defaults to "". 
        """

        self.dimension = {'m':0,'kg':0,'s':0,'A':0,'K':0,'mol':0,'cd':0}

        self.name = name

        self.description = description

        self._re_eval_dimensions(dimension_dict)

    def _is_dimensionless(self):
        """
        Check if the current Unit object is adimensional.

        :return:
            Boolean return of the function, checking if the unit is adimensional or not
        :rtype Bool _is_dimensionless:
        """

        #is_dimless = all([float(self.dimension[idx_i]) == 0. for idx_i in keys_])

        is_dimless = all(float(d_i) == 0. for d_i in self.dimension.values())

        return is_dimless

    def _return_proto_unit(self, name="", dimension_dict={""}, description=""):
        """
        Return a Unit class with given name and description (defaults to "").
        Used for return of an Unit object as the result of unit operations, with dimension given by dimension_dict.

        :param str name:
            Unit object name

        :param str description:
            Unit object description
    
        :param dict(float) dimension_dict:
            Dimensions of the Unit object to be returned

        :return:
            Unit object returned
        :rtype Unit proto_unit:
        """

        return self.__class__(name, dimension_dict, description) 

    def _reset_dimensions(self, null_dimension):
        """
        Private function for reseting the dimensions of the present unit,
        using predefined null dimension.

        :param dict(float) null_dimension:
        Dictionary containing new dimension to reset the Unit object.
        Defaults to null_dimension predefined.
        """

        self.dimension = null_dimension

    def _re_eval_dimensions(self, dimension_dict):
        """
        Private function for redefinition of the dimensions of the present unit, using predefined null dimension.

        :param (dict(float) or Unit) dimension_dict:
        Dictionary (or proper unit) containing new dimension to redefine the Unit object. 

        """

        if isinstance(dimension_dict,dict) != True: #dimension_dict holds an Unit

            dimension_dict = dimension_dict.dimension

        for (dim_i, idx_i) in zip(dimension_dict.keys(), dimension_dict.values()):

            try:

                self.dimension[dim_i] = idx_i
                
            # If the present unit (self) does not contain the dimension 'dim_i', 
            # revert to null_dimension
            except KeyError:

                self.dimension[dim_i] = null_dimension[dim_i]

    def __mul__(self, other_unit):
        """
        Overloaded function for multiplication of two units with subsequent
        summation of its dimensions. As by definition the overloaded function returns
        a new dimensional dict, typical usage scenario is the definition of units
        derived from base-ones (eg:m * m = m²).

        :param Unit other_unit:
            Other unit for multiplication.

        :return:
            New unit returned by the arithmetic operation between two primitive units,
            with corresponding dimension.
        :rtype Unit new_unit:
        """

        new_dimension = copy.copy(other_unit.dimension)

        for (dim_i, idx_i) in zip(self.dimension.keys(), self.dimension.values()):

            try:

                new_dimension[dim_i] = new_dimension[dim_i] + idx_i

            except KeyError:  # Second unit (other_unit) has no dimension 'dim_i' defined

                new_dimension[dim_i] = idx_i

        new_unit = self._return_proto_unit(dimension_dict=new_dimension)

        return new_unit

    def __div__(self, other_unit):
        """
        Overloaded function for division of two units with subsequent subtraction of its
        dimensions. As by definition the overloaded function returns a new dimensional dict,
        typical usage scenario is the definition of units
        derived from base-ones (eg:m / s = m/s).

        :param Unit other_unit:
            Other unit for division.

        :return:
            New unit returned by the arithmetic operation between two primitive units,
            with corresponding dimension.
        :rtype Unit new_unit:
        """

        new_dimension = copy.copy(other_unit.dimension)

        for (dim_i, idx_i) in zip(new_dimension.keys(), new_dimension.values()):

            try:

                new_dimension[dim_i] = self.dimension[dim_i] - idx_i

            except KeyError:  # First unit (self) has no dimension 'dim_i' defined

                new_dimension[dim_i] = -idx_i

        new_unit = self._return_proto_unit(dimension_dict=new_dimension)

        return new_unit

    def __pow__(self, power):
        """
        Overloaded function for power of one units with subsequent doubling of its dimensions (x2).
        As by definition the overloaded function returns a new dimensional dict,
        typical usage scenario is the definition of units redived from base-ones (eg:m ** 2 = m²).

        :param float power:
            Power for operation with the unit(self).

        :return:
            New unit returned by the arithmetic operation, with corresponding dimension.
        :rtype Unit new_unit:
        """

        new_dimension = copy.copy(self.dimension)

        for (dim_i, idx_i) in zip(self.dimension.keys(), self.dimension.values()):

            new_dimension[dim_i] = idx_i*power

        new_unit = self._return_proto_unit(dimension_dict=new_dimension)

        return new_unit

    def _check_dimensional_coherence(self, other_unit):
        """
        Function for quick checking of dimensional coherence between two units.

        :param Unit other_unit:
            Second unit to be tested

        :return:
            Return if the dimension between both units are equal.
        :rtype bool:
        """

        keys_ = sorted(self.dimension.keys())

        """
        Syntatic convenience vodoo for conversion of dimensions of both units to one single str object.
        Thus the comparison between the two Unit objects is easy

        [str() for ...] -> List of each dimension converted to str

        "".join() -> Concatenation of str objects in one single string
        
        """

        dim_1 = "".join([str(float(self.dimension[idx_i])) for idx_i in keys_])

        dim_2 = "".join([str(float(other_unit.dimension[idx_i])) for idx_i in keys_])

        return dim_1 == dim_2
