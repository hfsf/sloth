"""
Define Equation class.
Creates objects that holds equations and re-evaluates its value using the literal definition of the equation provided

Define functions for utilization in the equation definition
"""

import numpy as np
import expression_evaluation


#=====================================================================================================
"""
Unary functions for utilization in the equation definition
"""

def Log(obj):

    """
    Return a ExpressionTree branch-root containing an EquationNode for which the EquationNode.Log function is defined.
    """
    
    branch_root_node =  expression_evaluation.EquationNode( 
                                name = "Log ( " + obj.object.name + " )", \
                                base_object = None, \
                                base_operation = expression_evaluation.EquationNode.Log, \
                                base_operation_name = 'log'
                              )

    branch_root = expression_evaluation.ExpressionTree( object_ = branch_root_node )

    obj.parent = branch_root

    return(branch_root)

def Log10(obj):

    """
    Return a ExpressionTree branch-root containing an EquationNode for which the EquationNode.Log10 function is defined.
    """
    
    branch_root_node =  expression_evaluation.EquationNode( 
                                name = "Log10 ( " + obj.object.name + " )", \
                                base_object = None, \
                                base_operation = expression_evaluation.EquationNode.Log10, \
                                base_operation_name = 'log10'
                              )

    branch_root = expression_evaluation.ExpressionTree( object_ = branch_root_node )

    obj.parent = branch_root

    return(branch_root)

def Abs(obj):

    """
    Return a ExpressionTree branch-root containing an EquationNode for which the EquationNode.Abs function is defined.
    """
    
    branch_root_node =  expression_evaluation.EquationNode( 
                                name = "Abs ( " + obj.object.name + " )", \
                                base_object = None, \
                                base_operation = expression_evaluation.EquationNode.Abs, \
                                base_operation_name = 'abs'
                              )

    branch_root = expression_evaluation.ExpressionTree( object_ = branch_root_node )

    obj.parent = branch_root

    return(branch_root)

def Exp(obj):

    """
    Return a ExpressionTree branch-root containing an EquationNode for which the EquationNode.Exp function is defined.
    """
    
    branch_root_node =  expression_evaluation.EquationNode( 
                                name = "Exp ( " + obj.object.name + " )", \
                                base_object = None, \
                                base_operation = expression_evaluation.EquationNode.Exp, \
                                base_operation_name = 'exp'
                              )

    branch_root = expression_evaluation.ExpressionTree( object_ = branch_root_node )

    obj.parent = branch_root

    return(branch_root)

def Sin(obj):

    """
    Return a ExpressionTree branch-root containing an EquationNode for which the EquationNode.Sin function is defined.
    """
    
    branch_root_node =  expression_evaluation.EquationNode( 
                                name = "Sin ( " + obj.object.name + " )", \
                                base_object = None, \
                                base_operation = expression_evaluation.EquationNode.Sin, \
                                base_operation_name = 'sin'
                              )

    branch_root = expression_evaluation.ExpressionTree( object_ = branch_root_node )

    obj.parent = branch_root

    return(branch_root)

def Cos(obj):

    """
    Return a ExpressionTree branch-root containing an EquationNode for which the EquationNode.Cos function is defined.
    """
    
    branch_root_node =  expression_evaluation.EquationNode( 
                                name = "Cos ( " + obj.object.name + " )", \
                                base_object = None, \
                                base_operation = expression_evaluation.EquationNode.Cos, \
                                base_operation_name = 'cos'
                              )

    branch_root = expression_evaluation.ExpressionTree( object_ = branch_root_node )

    obj.parent = branch_root

    return(branch_root)

def Tan(obj):

    """
    Return a ExpressionTree branch-root containing an EquationNode for which the EquationNode.Tan function is defined.
    """
    
    branch_root_node =  expression_evaluation.EquationNode( 
                                name = "Tan ( " + obj.object.name + " )", \
                                base_object = None, \
                                base_operation = expression_evaluation.EquationNode.Tan, \
                                base_operation_name = 'tan'
                              )

    branch_root = expression_evaluation.ExpressionTree( object_ = branch_root_node )

    obj.parent = branch_root

    return(branch_root)

#=====================================================================================================

class Equation:

    """

    Equation class


    TODO: Insert curatorship mechanism for DOF, through the analysis of the declares object for each equation.

    """

    def __init__(self, name, description, fast_expr = None):

        """
        Inidial definitions.

        :param str name:
        Name for the current equation

        :param str description:
        Description for the present equation. Defauls to ""

        :param ExpressionTree fast_expr:
        ExpressionTree object to declare for the current Equation object.  If declared, the moethod '.setResidual' are executed as a shortcut. Defaults to None.
        
        """

        self.name = name

        self.description = description

        #Residual of the current equation

        self.residual = None

        self.equation_expression = None

        self._equation_expression_ = None

        self.objects_declared = {}

        if fast_expr != None:

            self.setResidual( fast_expr )

    def setResidual(self, equation_expression):

        """
    
        Creates the equation using the 'equation_expression' (ExpressionTree), storing it for posterior utilization.

        :param equation_str:
        String containing equation definition (eg: 'self.a + self.b*Log10(self.c*self.R)').

        """

        self.equation_expression = equation_expression

        self._equation_expression_ = equation_expression

        self.objects_declared = self.equation_expression._sweep_()

    def resolveResidual(self):

        """

        Update the equation of residuals using the 'equation_expression' preivously defined

        """

        self.setResidual( self._equation_expression_ )

    def evalResidual(self):

        self.equation_expression._evalExpressionTree_()


class Connection(Equation):

    def __init__(self, name, description, fast_expr = None):

        """
        Inidial definitions.

        :param str name:
        Name for the current equation

        :param str description:
        Description for the present equation. Defauls to ""

        :param ExpressionTree fast_expr:
        ExpressionTree object to declare for the current Equation object.  If declared, the moethod '.setResidual' are executed as a shortcut. Defaults to None.
        
        """
