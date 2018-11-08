
# *coding:utf-8*

import sympy as sp
from scipy.linalg import solve

class EquationBlock:

    """
    Define EquationBlock. Act as a container for Equation objects and provides mechanisms for transforming them into matrix form. 
    """

    def __init__(self, equations, owner_model=None):

        """
        Instantiate EquationBlock

        :ivar Model owner_model:
            Model for which the EquationBlock is defined

        :ivar dict(Equations) equations:
            Dictionary containing the Equation objects for the EquationBlock. Defaults to the whole set of equations from the owner model.
        """

        self.owner_model = owner_model

        self.equations = equations

        self._var_list = []

        self._equations_list = []

        self._matrix_A = None

        self._matrix_b = None

    def _getVarList(self):

        """
        Set the list for each of the Variable objects that appear in the equations of the model
        
        :return:
            List of variable names
        :rtype list(Variable):
        
        # TODO
            * Optimize code snippet marked below
        """

        var_list = []

        # ========== NEEDS TO BE OPTIMIZED ==========

        for  eq_i in self.equations:

            for var_i in list(eq_i.objects_declared.values()):

                if var_i not in self._var_list:

                    var_list.append(var_i)

        # ===========================================

        return var_list

    def _getEquationList(self):

        """
        Set the list of sympy expressions representing the equation.

        :return:
            List of the sympy expressions representing each Equation object of the model

        :rtype list(sympy expresion):
        """

        return [eq_i.symbolic_object for eq_i in self.equations]

    def _getCoeffsFromEquations(self, eq_list, declared_objs):

        """
        Return two Matrix objects corresponding to A and b (Ax - b = 0) from the list of equations

        :param list(Equations) eq_list:
            List of Equation objects from which the coefficients will be extracted

        :param list(sympy.symbol) declared_objs:
            List of symbolic objects from which the coefficient matrix should be determined

        :return:
            Coefficient matrix (A) and array (b) representing the equations

        :rtype tuple(Matrix, Matrix): 
        """

        return sp.linear_eq_to_matrix(eq_list, declared_objs)

    def __call__(self):

        """
        Overloaded method for EquationBlock object. Examines the equations atribute of the EquationBlock object and build the matrix 
        """

        # Fill-up the list of Variables and Equations

        self._var_list = self._getVarList()

        self._equations_list = self._getEquationList()

        self._matrix_A, \
        self._matrix_b = self._getCoeffsFromEquations(self._equations_list, \
                                                      self._var_list
                                                      )
    def solve(self):

        """
        Solve the current linear system defined in the class atributes

        :return:
            Solution for the linear system defined
        :rtype ndarray:
        """

        return solve(self._matrix_A, self._matrix_b)
