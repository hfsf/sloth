# *coding:utf-8*

"""
Define Equation class.Creates objects that holds equations and re-evaluates its value using the literal definition of the equation provided

Define Connection class. Special type of Equation that are used as source or sink terms (process inlet or outlet, respectively) or to connect two different Model objects.
"""

from .expression_evaluation import EquationNode
from .error_definitions import UnexpectedValueError, AbsentRequiredObjectError, UnresolvedPanicError
import sympy as sp
#import symengine as sp
import threading

_uid = threading.local()

def gen_rnd_str():

    if getattr(_uid, "uid", None) is None:
        _uid.tid = threading.current_thread().ident
        _uid.uid = 0
    _uid.uid += 1
    return str((_uid.tid, _uid.uid)[1])

class Equation:

    """
    Definition of Equation class. Process the ExpressionNode into one resultant node, which can be evaluated.
    """

    def __init__(self, name, description, fast_expr=None, owner_model_name=""):

        """
        Istantiate Equation.

        :ivar str name:
            Name for the current equation

        :ivar str description:
            Description for the present equation. Defauls to ""

        :ivar EquationNode fast_expr:
            EquationNode object to declare for the current Equation object. Defaults to None.

        :ivar str owner_model_name:
            Name of the owner model of the current Equation object. Defaults to "", meaning that the object was created aside a model.

        """

        if name is "":

            name = gen_rnd_str()

        #print("===> fast_expr = ", fast_expr,", owner_model_name = ", owner_model_name)

        self.name = name

        self.description = description

        self.residual = None

        self.equation_expression = None

        self.elementary_equation_expression = None

        self.equation_form = 'residual'

        self.type = None

        self.objects_declared = {}

        if fast_expr is not None:

            self.setResidual(fast_expr)

        self.owner_model_name = owner_model_name

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

    def _getSymbolicObject(self, equation_form=None, side='rhs'):

        """
        Return the symbolic_object atribute of the EquationNode contained in the equation_expression atribute of the current Equation object

        :param str equation_form:
            Determine the form of the equation, if it is in the residual form (y - a*x - b == 0) or elementary form (y == a*x + b). Defaults to None, for which the equation form defined in the equation_form atribute is used

        :param str side:
            Determine which side of the equation should be examined to return the symbolic object. Valid only for those defined in the elementary form. Defaults to "rhs"

        :return symbolic_object_:
            Dictionary containing the mapping beetween the symbolic objects (sympy.Symbol) and their corresponding Quantity objects
        """

        if equation_form == None:

            equation_form = self.equation_form

        if equation_form == 'residual':

            return self.equation_expression.symbolic_object

        elif equation_form == 'elementary' and side is 'lhs':

            return self.elementary_equation_expression[0].symbolic_object

        elif equation_form == 'elementary' and side is 'rhs':

            return self.elementary_equation_expression[1].symbolic_object

        else:

            raise UnresolvedPanicError()

    def _getSymbolicMap(self, equation_form=None, side='rhs'):

        """
        Return the symbolic_map atribute of the EquationNode contained in the equation_expression atribute of the current Equation object

        :param str equation_form:
            Determine the form of the equation, if it is in the residual form (y - a*x - b == 0) or elementary form (y == a*x + b). Defaults to None, for which the equation form defined in the equation_form atribute is used

        :param str side:
            Determine which side of the equation should be examined to return the symbolic map. Valid only for those defined in the elementary form. Defaults to "rhs"

        :return symbolic_map_:
            Dictionary containing the mapping beetween the symbolic objects (sympy.Symbol) and their corresponding Quantity objects
        """

        if equation_form == None:

            equation_form = self.equation_form

        if equation_form == 'residual':

            return self.equation_expression.symbolic_map

        elif equation_form == 'elementary' and side is 'lhs':

            return self.elementary_equation_expression[0].symbolic_map

        elif equation_form == 'elementary' and side is 'rhs':

            return self.elementary_equation_expression[1].symbolic_map

        else:

            raise UnresolvedPanicError()

    def _sweepObjects(self):

        """
        Examines the symbolic objects declared in the current equation and store in the objects_declared atribute.
        Note: This function is intended to be internally executed.
        """

        # This code snippet work only on Python 3.5+

        self.objects_declared = { **self.equation_expression.symbolic_map }

    def _convertToResidualForm(self):

        """
        Convert differential equations from the elementary form to the residual form (eg: u' == u + v  becomes u' -(u+v) )
        """

        self._getTypeFromExpression()

        if self.type == "differential" and self.equation_form != "residual":

            self.equation_expression = self.elementary_equation_expression[0] - self.elementary_equation_expression[1]

            self.equation_form = "residual"

    def _convertToFunction(self, symbolic_map=None, side=None, compilation_mechanism='llvm'):

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

    def _convertEquationSymbolicExpression(self, names_map, whole_obj_map):

        """
        Convert the symbolic representation of the equation using a dictionary for mapping

        :param dict names_map:
            Dictionary for mapping the symbolic representation (names) used in the symbolic conversion
                replacing 'a_M2' for 'a_M1' (e.g: {'a_M1':'a_M2'})

       :param dict whole_obj_map:
            Dictionary for mapping the  symbolic representation and their correspondent for ALL objects in the
                model following form: {'a_M1':Variable(), ...}. Used for rwrite the symbolic_map of the rewrited
                equation_expression object.
        """

        self.equation_expression.repr_symbolic = self.equation_expression.repr_symbolic.subs(names_map)

        self.equation_expression.symbolic_object = self.equation_expression.symbolic_object.subs(names_map)

        if self.elementary_equation_expression is not None:

            elem_expr = list(self.elementary_equation_expression)

            elem_expr[0].repr_symbolic = elem_expr[0].repr_symbolic.subs(names_map)

            elem_expr[1].repr_symbolic = elem_expr[1].repr_symbolic.subs(names_map)

            try:

                elem_expr[0].symbolic_object = elem_expr[0].symbolic_object.subs(names_map)

            except:

                pass #Element does not support symbolic substitution. It is a float.

            try:

                elem_expr[1].symbolic_object = elem_expr[1].symbolic_object.subs(names_map)

            except:

                pass #Element does not support symbolic substitution. It is a float.

            symbols_used_0 = [str(i) for i in list(elem_expr[0].repr_symbolic.free_symbols)]

            symbols_used_1 = [str(i) for i in list(elem_expr[1].repr_symbolic.free_symbols)]

            elem_expr[0].symbolic_map = {k:whole_obj_map[k] for k in symbols_used_0}

            elem_expr[1].symbolic_map = {k:whole_obj_map[k] for k in symbols_used_1}

            self.elementary_equation_expression = tuple(elem_expr)

        symbols_used_ = [str(i) for i in list(self.equation_expression.repr_symbolic.free_symbols)]

        new_symbolic_map = {k:whole_obj_map[k] for k in symbols_used_}

        self.equation_expression.symbolic_map = new_symbolic_map

        self._sweepObjects()

    def setResidual(self, equation_expression):

        """
        Creates the equation using the 'equation_expression', storing it for posterior utilization.

        :ivar EquationNode, tuple(EquationNode,EquationNode) equation_expression:
        EquationNode containing the equation definition in the residual form (eg: self.a() + self.b() -self.c() = 0) or in the elementar form (self.a()+self.b() == self.c()).

        """

        if isinstance(equation_expression, tuple) and isinstance(equation_expression[0], EquationNode):

            # The equation expression is in the elementary form

            if isinstance(equation_expression[1], EquationNode):

                #If the RHS is an ENODE, pass it directly

                self.elementary_equation_expression = tuple([equation_expression[0], equation_expression[1]])

                self.equation_expression = equation_expression[0] - equation_expression[1]

            if isinstance(equation_expression[1], float) or isinstance(equation_expression[1], int):

                #If the RHS is a float or an int, convert it to ENODE previously

                equation_expression1_as_enode = EquationNode(name='constant'+gen_rnd_str(),
                                                             symbolic_object=equation_expression[1],
                                                             unit_object=equation_expression[0].unit_object,
                                                             repr_symbolic=equation_expression[1])

                self.elementary_equation_expression = tuple([equation_expression[0], equation_expression1_as_enode])

                self.equation_expression = equation_expression[0] - equation_expression1_as_enode

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

            symbolic_map_ = self.equation_expression.symbolic_map

        else:

            symbolic_map_ = symbolic_map

        eq_keys=symbolic_map_.keys()

        eq_values=symbolic_map_.values()

        eval_map = dict( ( (i,j) for i, j in zip(eq_keys,eq_values) ) )

        if isinstance(equation_expression_.symbolic_object, float) or isinstance(equation_expression_.symbolic_object, int):

            res = equation_expression_.symbolic_object

        else:

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
