"""
Define variable class.
"""

from .quantity import Quantity
from .equation_operators import _Diff
from .error_definitions import AbsentRequiredObjectError
from .domain import Domain

class Variable(Quantity):

    """

    Variable class definition, that holds capabilities for:
    - Variable definition, including its units for posterior dimensional coherence analysis
    - Variable operations using overloaded mathematical operators, making possible an almost-writing-syntax (eg: a() + b() )

    """

    def __init__(self, name, units , description = "", is_lower_bounded = False, is_upper_bounded = False, lower_bound = None, upper_bound = None,  value = 0, is_exposed=False, type='', latex_text="", owner_model_name="", domain=None):


        super().__init__(name, units, description, value, latex_text, owner_model_name)

        """
        Initial definition.

        :param str name:
            Name for the current variable

        :param Unit units:
            Definition of dimensional unit of current variable

        :param str description:
            Description for the present variable. Defauls to ""

        :param bool is_exposed:
        Define if the Variable object will be treated as an exposed variable for a Model object

        :param str type:
        Determines the exposure type of the variable object. Can be 'input', 'output' or None, for non-exposed objects.

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

        :param bool is_exposed:
            If the current Variable object is exposed in its owner model or not. Defaults to False.

        :param str type:
            The exposure type of the current Variable object in its owner model. Defaults to '', meaning that the object is not exposed.

        :param str latex_text:
            Text for latex representation.

        :param Domain domain:
            Domain

        :ivar str owner_model_name:
            Name of the owner model of the current Quantity object. Defaults to "", meaning that the object was created aside a model.

        === Coming from base class ===

        self.name = name

        self.units = units

        self.description = description

        self.value = value

        self.owner_model_name = owner_model_name

        """

        self.is_lower_bounded = ( lower_bound != None )

        self.is_upper_bounded = ( upper_bound != None )

        self.lower_bound = lower_bound

        self.upper_bound = upper_bound

        self.domain = domain

        self.is_exposed = is_exposed

        self.type = type

    def distributeOnDomain(self, domain):

        """
        Function for registration of the current Variable object into one Domain object.

        :param Domain domain:
            Domain in which the current Variable object should be distributed
        """

        self.domain = domain

        domain._distributeOnDomain(self)

        domain._setDomain()

    def Diff(self, ind_var=None):

        """
        Function for calculation of the time derivative of the Variable object. Require that the Variable object is distributed in a dynamic domain.
        """

        if self.domain != None:

            return _Diff(self, ind_var)

        else:

            raise AbsentRequiredObjectError("Domain")






