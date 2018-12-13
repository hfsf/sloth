"""
Define parameter class.
"""

from .quantity import Quantity
from .error_definitions import UnexpectedValueError, DimensionalCoherenceError


class Parameter(Quantity):

    """

    Parameter class definition, that holds capabilities for:
    - Parameter definition, including its units for posterior dimensional coherence analysis
    - Parameter operations using overloaded mathematical operators, making possible an almost-writing-syntax (eg: a() + b() )

    """


    def __init__(self, name, units , description="", value=0, latex_text="", is_specified=False):

        super().__init__(name, units, description, value, latex_text)

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

        self.is_specified = is_specified

    def setValue(self, quantity_value, quantity_unit=None):

        """
        Method for value specification of Parameter object. Overloaded from base class Quantity.

        :param [float, Quantity] quantity_value:
            Value to the current Parameter object

        :param Unit quantity_unit:
            Unit object for the parameter. Defaults to currennt units
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