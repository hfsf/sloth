#*coding:utf-8*

"""
Define Unit class, for ulterior utilization (eg:Variable,Parameter)

Define the UnitContainingObject (UCO), base-class for all unit-containg objects (Variables, Parameters, Constants)
"""

import copy

class UnitContainingObject:

       """

       Return an Unit-Containing object (UCO) class with given name, description and other variables (defaults to "", False and None, when aplicable). Used for return of an Variable object as the result of variable operations, with dimension given by units

       :param str name:
       Name for the current UCO

       :param Unit units:
       Definition of dimensional unit of current UCO

       :param str description:
       Description for the present UCO. Defauls to ""

       """

    def __init__(self, name, units, description = "", value = 0.):

        """

        Initial definition.

        :param str name:
        Name for the current Unit-Containing Object (UCO)

        :param Unit units:
        Definition of dimensional unit of current UCO

        :param str description:
        Description for the present UCO. Defauls to ""

        :param float value:
        Value of the current UCO. Defaults to 0.  

        """

        self.name = name

        self.units = units

        self.description = description

        self.value = value


    def _returnProtoObject(self, name="", units={""}, description = "", value = 0):

       """

       Return a Proto Unit-Containing object (UCO) class with given name, description and other variables (defaults to "", False and None, when aplicable). Used for return of an Variable object as the result of variable operations, with dimension given by units

       :param str name:
       Name for the current UCO

       :param Unit units:
       Definition of dimensional unit of current UCO

       :param str description:
       Description for the present UCO. Defauls to ""

       """

        return( self.__class__(name=name, units=units, description=description, value = value) )

    def __add__(self, other_var):

        """

        Overloaded function for summation of two unit-containing-objects.
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

        Overloaded function for subtraction of two unit-containing-objects.
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

        Overloaded function for multiplication of two unit-containing-objects.
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

        Overloaded function for division of two unit-containing-objects.
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

        Overloaded function for exponentiation of one unit-containing-object.
        The __pow__ function does not requires dimensional coherence, but resultant variable units should be modified

        :param float power:
        Power for operation with the unit(self).

        :rtype Variable new_var:
        Proto-variable returned as the result of the arithmetical operation

        """

        new_var = self._returnProtoVariable(units = self.units**power, value = self.value**power)

        return(new_var) 

class Unit:

    null_dimension = {'m':0,'kg':0,'s':0,'A':0,'K':0,'mol':0,'cd':0}


    """

    Unit class definition, that holds the capabilities:
    - Dictinary containing the dimensional index for each SI dimension, used in dimensional coherence analysis in proper classes (eg: Variable, Parameter)
    - Unit operations using overloaded mathematical operators (multiplication, division, power), making possible an almost-writing-syntax

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

        self._reEvalDimensions(dimension_dict)

    def _returnProtoUnit(self, name="", dimension_dict={""}, description = ""):

        """
        
        Return a Unit class with given name and description (defaults to ""). Used for return of an Unit object as the result of unit operations, with dimension given by dimension_dict.

        :param dict(float) dimension_dict:
        Dimensions of the Unit object to be returned

        :rtype Unit proto_unit:
        Unit object returned       

        """

        return( self.__class__(name, dimension_dict, description) )

    def _resetDimensions(self, dimension_dict = null_dimension):

        """

        Private function for reseting the dimensions of the present unit, using predefined null dimension.

        :param dict(float) dimension_dict:
        Dictionary containing new dimension to reset the Unit object. Defaults to null_dimension predefined. 

        """

        self.dimension = null_dimension

    def _reEvalDimensions(self, dimension_dict):

        """

        Private function for redefinition of the dimensions of the present unit, using predefined null dimension.

        :param (dict(float) or Unit) dimension_dict:
        Dictionary (or proper unit) containing new dimension to redefine the Unit object. 

        """

        if isinstance(dimension_dict,dict) != True: #dimension_dict holds an Unit

            dimension_dict = dimension_dict.dimension


        for (dim_i,idx_i) in zip(dimension_dict.keys(),dimension_dict.values()):

            try:

                self.dimension[dim_i] = idx_i

            except KeyError: #If the present unit (self) does not contain the dimension 'dim_i', revert to null_dimension

                self.dimension[dim_i] = null_dimension[dim_i]

    def __mul__(self, other_unit):

        """
        Overloaded function for multiplication of two units with subsequent summation of its dimensions.
        As by definition the overloaded function returns a new dimensional dict, typical usage scenario is the
         definition of units redived from base-ones (eg:m * m = m²).

        :param Unit other_unit:
        Other unit for multiplication.

        :rtype Unit new_unit:
        New unit returned by the arithmetic operation between two primitive units, with corresponding dimension.

        """

        new_dimension = copy.copy(other_unit.dimension)

        for (dim_i,idx_i) in zip(self.dimension.keys(),self.dimension.values()):

            try:

                new_dimension[dim_i] = new_dimension[dim_i] + idx_i

            except KeyError: #Second unit (other_unit) has no dimension 'dim_i' defined

                new_dimension[dim_i] = idx_i

        new_unit = self._returnProtoUnit(dimension_dict=new_dimension)

        return(new_unit)

    def __div__(self, other_unit):

        """
        Overloaded function for division of two units with subsequent subtraction of its dimensions.
        As by definition the overloaded function returns a new dimensional dict, typical usage scenario is the
         definition of units redived from base-ones (eg:m / s = m/s).

        :param Unit other_unit:
        Other unit for division.

        :rtype Unit new_unit:
        New unit returned by the arithmetic operation between two primitive units, with corresponding dimension.

        """

        new_dimension = copy.copy(other_unit.dimension)

        for (dim_i,idx_i) in zip(new_dimension.keys(), new_dimension.values()):

            try:

                new_dimension[dim_i] = self.dimension[dim_i] - idx_i

            except KeyError: #First unit (self) has no dimension 'dim_i' defined

                new_dimension[dim_i] = -idx_i

        new_unit = self._returnProtoUnit(dimension_dict=new_dimension)

        return(new_unit)


    def __pow__(self, power):

        """
        Overloaded function for power of one units with subsequent doubling of its dimensions (x2).
        As by definition the overloaded function returns a new dimensional dict, typical usage scenario is the
         definition of units redived from base-ones (eg:m ** 2 = m²).

        :param float power:
        Power for operation with the unit(self).


        :rtype Unit new_unit:
        New unit returned by the arithmetic operation, with corresponding dimension.

        """

        new_dimension = copy.copy(self.dimension)

        for (dim_i,idx_i) in zip(self.dimension.keys(),self.dimension.values()):

            new_dimension[dim_i] = idx_i*power

        new_unit = self._returnProtoUnit(dimension_dict=new_dimension)

        return(new_unit)

    def _checkDimensionalCoherence(self, other_unit):

        """
        Function for quick checking of dimensional coherence between two units.

        :param Unit other_unit:
        Second unit to be tested

        :rtype bool:
        Return if the dimension between both units are equal.
        """

        keys_ = sorted(self.dimension.keys())

        """
        Syntatic convenience vodoo for conversion of dimensions of both units to one single str object.
        Thus the comparison between the two Unit objects is easy

        [str() for ...] -> List of each dimension converted to str

        "".join() -> Concatenation of str objects in one single string
        
        """

        dim_1 = "".join([str(self.dimension[idx_i]) for idx_i in keys_])

        dim_2 = "".join([str(other_unit.dimension[idx_i]) for idx_i in keys_])

        return(dim_1==dim_2)