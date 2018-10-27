# *coding:utf-8*

"""
Define Equation class.
Creates objects that holds equations and re-evaluates its value using the literal definition of the equation provided
"""

#==================================================================================

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

        self.objects_declared = {}

        if fast_expr != None:

            self.setResidual( fast_expr )

    def _sweepObjects(self):

        """
        Examines the symbolic objects declared in the current equation and store in the objects_declared atribute. 
        Note: This function is intended to be internally executed.
        """

        # This code snippet work only on Python 3.5+

        self.objects_declared = { **self.equation_expression.symbolic_map }

    def setResidual(self, equation_expression):

        """
        Creates the equation using the 'equation_expression', storing it for posterior utilization.

        :ivar EquationNode equation_str:
        EquationNode containing the equation definition (eg: 'self.a() + self.b()*Log10(self.c()*self.R())').

        """

        self.equation_expression = equation_expression

        self.objects_declared = self._sweepObjects()


    def evalResidual(self):

        """
        Map the symbolic objects defined into the equation_expression atribute in a numerical result, using the current value of the related quantity objects.
        """
        
        eq_keys=self.equation_expression.symbolic_map.keys()

        eq_values=self.equation_expression.symbolic_map.values()

        eval_map = dict( ( (i,j.value) for i, j in zip(eq_keys,eq_values) ) )

        res = self.equation_expression.symbolic_object.evalf(subs=eval_map)

        self.residual = res

    def getResidual(self):

        """
        Return the residual for the current Equation.

        :return:
            Residue value for the current equation
        :rtype float:
        """

        self.evalResidual()

        return(self.residual)