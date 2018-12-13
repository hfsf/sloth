"""

Define Connection class.
- Special type of Equation that are used as source or sink terms (process inlet or outlet, respectively) or to connect two different Model objects.

"""

from .core.equation import *

class Connection(Equation):

    def __init__(self, name, description, output_var_name = "", input_var_name = "", fast_expr = None):

        super().__init__(name, description, fast_expr)

        """
        Instantiate Connection

        :ivar str name:
            Name for the current equation

        :ivar str description:
            Description for the present equation. Defaults to ""

        :ivar str output_var_name:
            Name of the output Variable object linked to the input Variable object through the current Connection object. Defaults to ""

        :ivar str input_var_name:
            Name of the input Variable object linked to the output Variable object through the current Connection object. Defaults to ""

        :ivar str description:
            Description for the present equation. Defaults to ""

        :ivar EquationNode fast_expr:
            EquationNode object to declare for the current Equation object.  If declared, the method '.setResidual' are executed as a shortcut. Defaults to None.
        
        """

        self.input_var_name = input_var_name

        self.output_var_name = output_var_name