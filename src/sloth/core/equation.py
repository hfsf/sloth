# *coding:utf-8*

"""
Define Equation class.Creates objects that holds equations and re-evaluates its value using the literal definition of the equation provided

Define Connection class. Special type of Equation that are used as source or sink terms (process inlet or outlet, respectively) or to connect two different Model objects.
"""

from .expression_evaluation import EquationNode
from .error_definitions import UnexpectedValueError, AbsentRequiredObjectError
import sympy as sp

class Equation:

    """
    Definition of Equation class. Process the ExpressionNode into one resultant node, which can be evaluated.
    """

    def __init__(self, name, description, fast_expr = None):

        """
        Istantiate Equation.

        :ivar str name:
        Name for the current equation

        :ivar str description:
        Description for the present equation. Defauls to ""

        :ivar EquationNode fast_expr:
        EquationNode object to declare for the current Equation object. Defaults to None.
        """

        self.name = name

        self.description = description

        self.residual = None

        self.equation_expression = None

        self.elementary_equation_expression = None

        self.equation_form = 'residual'

        self.type = None

        self.objects_declared = {}

        if fast_expr != None:

            self.setResidual( fast_expr )

    def __call__(self, i=1):

        """
        Return the EquationNode object represented by current Equation object.

        :param int i:
             The side of the equation to be returned, if the current Equation is defined in elementary form (0=left, 1 = right). Defaults to right hand side.

        :return enode_:
            EquationNode object represented by the current Equation
        :rtype EquationNode:
        """

        if self.equation_form == 'residual':

            return self.equation_expression

        if self.equation_form == 'elementary':

            try:

                return self.elementary_equation_expression[i]

            except:

                raise UnexpectedValueError("int")


    def _getTypeFromExpression(self):

        """
        Get the information about the current equation is algebraic linear, algebraic nonlinear or differential, determined from the equation expression (EquationNode) and set the attributes accordingly.
        """

        is_linear = self.equation_expression.equation_type['is_linear']

        is_nonlinear = self.equation_expression.equation_type['is_nonlinear']

        is_differential = self.equation_expression.equation_type['is_differential']

        if is_linear == True:

            self.type = 'linear'

        elif is_nonlinear == True:

            self.type = 'nonlinear'

        elif is_differential == True:

            self.type = 'differential'

        else:

            self.type = None

    def _sweepObjects(self):

        """
        Examines the symbolic objects declared in the current equation and store in the objects_declared atribute. 
        Note: This function is intended to be internally executed.
        """

        # This code snippet work only on Python 3.5+

        self.objects_declared = { **self.equation_expression.symbolic_map }

    def _convertToFunction(self, symbolic_map=None, side=None, compilation_mechanism='numpy'):

        """
        Convert the current equation expression into a function.
        
        :param dict symbolic_map:
            Symbolic map for value reference to the variables. Defaults to the symbolic map currently defined for the Equation object.

        :param str side:
            Which side of the equality should be evaluated (for Equation objects defined in the elementary form). 'lhs' for left hand side, 'rhs' for right hand side. Defaults to None, in which case an elementary formed Equation object is assumed.

        :param str compilation_mechanism:
            Which library are used in the compilation of the equations into functions. Include 'numexpr', 'mpmath', 'numpy'. Defaults to 'numpy'

        :return func:
            Returns the function corresponding to the expression of the current Equation object.
        :rtype function:
        """

        if side == None:
        
            equation_expression_ = self.equation_expression

        elif side == 'lhs' and self.elementary_equation_expression != None:

            equation_expression_ = self.elementary_equation_expression[0]

        elif side == 'rhs' and self.elementary_equation_expression != None:

            equation_expression_ = self.elementary_equation_expression[1]

        else:

            raise AbsentRequiredObjectError("Equation in elementary form")

        if symbolic_map == None:

            symbolic_map_ = self.equation_expression.symbolic_map

        else:

            symbolic_map_ = symbolic_map

        eq_keys = list(symbolic_map_.keys())

        #print("\nEquation line#166\n\neq_keys=%s equation_expression = %s"%(eq_keys, str(equation_expression_)))

        func = sp.lambdify(eq_keys, equation_expression_.symbolic_object, compilation_mechanism)

        return func

    def setResidual(self, equation_expression):

        """
        Creates the equation using the 'equation_expression', storing it for posterior utilization.

        :ivar EquationNode, tuple(EquationNode,EquationNode) equation_expression:
        EquationNode containing the equation definition in the residual form (eg: self.a() + self.b() -self.c() = 0) or in the elementar form (self.a()+self.b() == self.c()).

        """

        if isinstance(equation_expression, tuple) and \
           isinstance(equation_expression[0],EquationNode) and \
           isinstance(equation_expression[1], EquationNode):

            # The equation expression is in the elementary form

            self.elementary_equation_expression = tuple([equation_expression[0], equation_expression[1]])

            self.equation_expression = equation_expression[0] - equation_expression[1]

            self.equation_form = 'elementary'

            self.objects_declared = self._sweepObjects()

            self._getTypeFromExpression()

        elif isinstance(equation_expression, EquationNode):

            # The expression is in the residual form

            self.equation_expression = equation_expression

            self.objects_declared = self._sweepObjects()

            self._getTypeFromExpression()

        else:

            raise UnexpectedValueError("[EquationNode, tuple(EquationNode, EquationNode) ]")

    def eval(self, symbolic_map=None, side=None):

        """
        Map the symbolic objects defined into the equation_expression atribute in a numerical result, using the current value of the related quantity objects.

        :param dict symbolic_map:
            Symbolic map for value reference to the variables. Defaults to the symbolic map currently defined for the Equation object.

        :param str side:
            Which side of the equality should be evaluated (for Equation objects defined in the elementary form). 'lhs' for left hand side, 'rhs' for right hand side. Defaults to None.

        :return res:
            Returns the calculated value for the expression residual, given the symbolic mapping provided.
        :rtype float:
        """

        if side == None:
        
            equation_expression_ = self.equation_expression

        elif side == 'lhs' and self.elementary_equation_expression != None:

            equation_expression_ = self.elementary_equation_expression[0]

        elif side == 'rhs' and self.elementary_equation_expression != None:

            equation_expression_ = self.elementary_equation_expression[1]

        else:

            raise AbsentRequiredObjectError("Equation in elementary form")

        if symbolic_map == None:

            symbolic_map = self.equation_expression.symbolic_map

        else:

            symbolic_map_ = symbolic_map

        eq_keys=symbolic_map_.keys()

        eq_values=symbolic_map_.values()

        eval_map = dict( ( (i,j) for i, j in zip(eq_keys,eq_values) ) )

        res = equation_expression_.symbolic_object.evalf(subs=eval_map)

        return res

    def getResidual(self):

        """
        Return the residual for the current Equation.

        :return:
            Residue value for the current equation
        :rtype float:
        """

        return self.eval()

class Connection(Equation):

    def __init__(self, name, description, connection_type = 'source', fast_expr = None):

        super().__init__(name, description, fast_expr)

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
