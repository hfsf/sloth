"""

Define Connection class.
- Special type of Equation that are used as source or sink terms (process inlet or outlet, respectively) or to connect two different Model objects.

"""

from core.Equation import *

class base_(object):

    pass

class Connection(base_,Equation):

    def __init__(self, name, description, connection_type = 'source', fast_expr = None):

        super(self.__class__,self).__init__(name, description, fast_expr)

        """
        Inidial definitions.

        :param str name:
        Name for the current equation

        :param str description:
        Description for the present equation. Defauls to ""

        :param str connection_type:
        Type of the connection. Options are 'source', when a source term is declared (eg: process inlet); 'sink', when a sink term is declared (eq: process outlet); 'input', when a input from the other model output is declared (thus, a source term coming from the sink term from another model); 'output', when a output the output of a model is declared (used as input by another model). Defaults to 'source'.

        :param ExpressionTree fast_expr:
        ExpressionTree object to declare for the current Equation object.  If declared, the moethod '.setResidual' are executed as a shortcut. Defaults to None.
        
        """

        self.connection_type = connection_type