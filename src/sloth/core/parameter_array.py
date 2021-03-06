
"""
Define ParameterArray class
"""

from .parameter import Parameter
from .error_definitions import UnexpectedValueError, DimensionalCoherenceError

class ParameterArray(Parameter):

    """
    ParameterArray class, which aggregates all the functionality for the Parameter objects, but provide array-like capabilities
    """

    def __init__(self, name, size, units, description="", value=0, latex_text="", is_specified=False, owner_model_name=""):

        if isinstance(value, list) and len(value) != size:

            raise UnexpectedValueError("Monothonic value for ParameterArray, or a list of values with equivalent size of the ParameterArray")

        super().__init__(name, units, description, value, latex_text, owner_model_name)

        """
        Initial definition.

        :param str name:
            Name for the current parameter

        :param int size:
            Size for the current ParameterArray object

        :param Unit units:
            Definition of dimensional unit of current parameter

        :param str description:
            Description for the present parameter. Defauls to ""

        """

        self._size = size

        self.array = np.zeros(size, dtype=object)

        if isinstance(value, list):

            for i in range(size):

                self.array[i] = Parameter(self.name+"-"+str(i), self.units, self.description, self.value[i], self.latex_text, self.owner_model_name)

        else:

            for i in range(size):

                self.array[i] = Parameter(self.name+"-"+str(i), self.units, self.description, self.value, self.latex_text, self.owner_model_name)


    def __getitem__(self, id):

        return self.array[id]

    @property
    def size(self):

        return  self.array.size

    @size.setter
    self size(x):

        raise ValueError("Cannot directly set an atribute for an ParameterArray object.")