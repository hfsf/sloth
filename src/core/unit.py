# *coding:utf-8*

"""
Define Unit class, for ulterior utilization (eg:Variable,Parameter)
"""

import copy
from .error_definitions import DimensionalCoherenceError, UnexpectedValueError
from .quantity import Quantity
# Null dimension dict
null_dimension = {'m':0.0,'kg':0.0,'s':0.0,'A':0.0,'K':0.0,'mol':0.0,'cd':0.0}

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

    def __str__(self):

        """
        Overloaded function for printing out the dimension of the Unit object in a convenient way. Eg: str({m:1 kg:0 s:-1 ... }) = 'm^1 s^-1'

        :return:
            Dimension of the current Unit object in a convenient way
        :rtype str output:
        """

        output=''

        output = [dim_i+"^"+str(self.dimension[dim_i]) for dim_i in list(self.dimension.keys()) if self.dimension[dim_i] != 0]

        output = " ".join(output)

        return output

    def __add__(self, other_unit):
        """
        Overloaded function for summation of two units . As by definition the overloaded function returns the same unit if dimensional coherence is confirmed, or raise a error otherwise (retuning None).

        :param Unit other_unit:
            Other unit for summation.

        :return:
            New unit returned by the arithmetic operation between two primitive units,
            with corresponding dimension.
        :rtype Unit new_unit:
        """

        if self._check_dimensional_coherence(other_unit) == True:

            return(self)

        else:

            raise DimensionalCoherenceError(self,other_unit)

            return(None)

    def __sub__(self, other_unit):
        """
        Overloaded function for subtraction of two units . As by definition the overloaded function returns the same unit if dimensional coherence is confirmed, or raise a error otherwise (retuning None).

        :param Unit other_unit:
            Other unit for subtraction.

        :return:
            New unit returned by the arithmetic operation between two primitive units,
            with corresponding dimension.
        :rtype Unit new_unit:
        """

        if self._check_dimensional_coherence(other_unit) == True:

            return(self)

        else:

            raise DimensionalCoherenceError(self,other_unit)

            return(None)

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

        if isinstance(other_unit, self.__class__):

            # other_unit is an Unit object

            new_dimension = copy.copy(other_unit.dimension)

            for (dim_i, idx_i) in zip(self.dimension.keys(), self.dimension.values()):

                try:

                    new_dimension[dim_i] = new_dimension[dim_i] + idx_i

                except KeyError:  # Second unit (other_unit) has no dimension 'dim_i' defined

                    new_dimension[dim_i] = idx_i

            new_unit = self._return_proto_unit(dimension_dict=new_dimension)

            return new_unit

        elif isinstance(other_unit, float) or isinstance(other_unit, int):

            # other_unit is an numerical value

            return Quantity("", self.__class__("", self.dimension), value=other_unit, latex_text=str(other_unit))

        else:

            raise UnexpectedValueError("(Unit, float, int)")


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
        if isinstance(other_unit, self.__class__):

            # other_unit is an Unit object

            new_dimension = copy.copy(other_unit.dimension)

            for (dim_i, idx_i) in zip(new_dimension.keys(), new_dimension.values()):

                try:

                    new_dimension[dim_i] = self.dimension[dim_i] - idx_i

                except KeyError:  # First unit (self) has no dimension 'dim_i' defined

                    new_dimension[dim_i] = -idx_i

            new_unit = self._return_proto_unit(dimension_dict=new_dimension)

            return new_unit

        elif isinstance(other_unit, float) or isinstance(other_unit, int):

            # other_unit is an numerical value

            return Quantity("", self.__class__("", self.dimension), value=1./other_unit, latex_text=str(other_unit))

        else:

            raise UnexpectedValueError("(Unit, float, int)")        


    def __truediv__(self, other_unit):
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

        if isinstance(other_unit, self.__class__):

            # other_unit is an Unit object

            new_dimension = copy.copy(other_unit.dimension)

            for (dim_i, idx_i) in zip(new_dimension.keys(), new_dimension.values()):

                try:

                    new_dimension[dim_i] = self.dimension[dim_i] - idx_i

                except KeyError:  # First unit (self) has no dimension 'dim_i' defined

                    new_dimension[dim_i] = -idx_i

            new_unit = self._return_proto_unit(dimension_dict=new_dimension)

            return new_unit

        elif isinstance(other_unit, float) or isinstance(other_unit, int):

            # other_unit is an numerical value

            return Quantity("", self.__class__("", self.dimension), value=1./other_unit, latex_text=str(other_unit))

        else:

            raise UnexpectedValueError("(Unit, float, int)")

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

        if isinstance(power, int) or isinstance(power, float):

            # power is a number.

            new_dimension = copy.copy(self.dimension)

            for (dim_i, idx_i) in zip(self.dimension.keys(), self.dimension.values()):

                new_dimension[dim_i] = idx_i*power

            new_unit = self._return_proto_unit(dimension_dict=new_dimension)

            return new_unit

        elif isinstance(power, self.__class__) and power._is_dimensionless():

            # power is another unit, presumably dimensionless

            new_unit = self._return_proto_unit(dimension_dict=self.dimension)

            return new_unit

        else:

            # power is not a number, neither a dimensionless unit.

            raise UnexpectedValueError("(int, float, dimensionless unit)")

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
