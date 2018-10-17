"""
Define Equation class.
Creates objects that holds equations and re-evaluates its value using the literal definition of the equation provided
"""

import numpy as np
import ExpressionEvaluation

class Equation:

    """

    Equation class


    TODO: Deprecate string-based equation creation and adopt expression tree paradigm

    """

    def __init__(self, name, description):

        """
        Inidial definitions.

        :param str name:
        Name for the current equation

        :param str description:
        Description for the present equation. Defauls to ""
        
        """

        self.name = name

        self.description = description

        #Residual of the current equation

        self.residual = None

        self.equation_expression = None

        self._equation_expression_ = None

        self.objects_declared = {}

    def setResidual(self, equation_expression):

        """
    
        Creates the equation using the 'equation_expression' (ExpressionTree), storing it for posterior utilization.

        :param equation_str:
        String containing equation definition (eg: 'self.a + self.b*Log10(self.c*self.R)').

        """

        self.equation_expression = equation_expression

        self._equation_expression_ = equation_expression

        self.objects_declared = self.equation_expression._sweepForObjects_()

    def resolveResidual(self):

        """

        Update the equation of residuals using the 'equation_expression' preivously defined

        """

        self.setResidual( self._equation_expression_ )

    def evalResidual(self):

        self.equation_expression._evalExpressionTree_()
