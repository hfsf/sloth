 
# *coding:utf-8*

import sympy as sp
from scipy.linalg import solve
from collections import OrderedDict

class EquationBlock:

    """
    Define EquationBlock. Act as a container for Equation objects and provides mechanisms for transforming them into matrix form. 
    """

    def __init__(self, equations, owner_model=None):

        """
        Instantiate EquationBlock

        :ivar list(Equations) equations:
            List containing the Equation objects for the EquationBlock. Defaults to the whole set of equations from the owner model.

        :ivar Model owner_model:
            Model for which the EquationBlock is defined. Defaults to None.
        """

        self.owner_model = owner_model

        self.equations = equations

        self._var_list = []

        self._var_dict = {}

        self._equations_list = []

        self._equation_groups = OrderedDict({'linear':[], 'nonlinear':[], 'differential':[]})

        self._assignEquationGroups()

    def _assignEquationGroups(self):

        """
        Get the type of each of the equations and assign them accordingly to the ._equation_groups atribute of the current EquationBlock object.
        """

        #print("\nEquation list: %s" %(self._equations_list))

        eq_lin = [i for i in self.equations if i.type == 'linear']

        eq_nlin = [i for i in self.equations if i.type == 'nonlinear']

        eq_diff = [i for i in self.equations if i.type == 'differential']

        self._equation_groups['linear'] = eq_lin

        self._equation_groups['nonlinear'] = eq_nlin

        self._equation_groups['differential'] = eq_diff

    def _getVarList(self):

        """
        Set the list for each of the Variable objects that appear in the equations of the model
        
        :return:
            List of variable names
        :rtype list(Variable):
        
        # TODO
            * Optimize code snippet marked below
        """

        # ========== NEEDS TO BE OPTIMIZED ==========

        var_name_list = []

        var_list = []

        for  eq_i in self.equations:

            for var_i in list(eq_i.objects_declared.values()):

                self._var_dict[var_i.name] = var_i

                if var_i not in var_list:

                    var_list.append(var_i)

                    var_name_list.append(var_i.name)



        # ===========================================

        return var_name_list

    def _getEquationList(self):

        """
        Set the list of sympy expressions representing the equation.

        :return:
            List of the sympy expressions representing each Equation object of the model

        :rtype list(sympy expresion):
        """

        return [eq_i.equation_expression.symbolic_object for eq_i in self.equations]

    def __call__(self):

        """
        Overloaded method for EquationBlock object. Examines the equations atribute of the EquationBlock object and build the matrix 
        """

        # Fill-up the list of Variables and Equations

        self._var_list = self._getVarList()

        self._equations_list = self._getEquationList()

        self._assignEquationGroups()

    def solve(self):

        """
        Solve the current linear system defined in the class atributes

        :return:
            Solution for the linear system defined
        :rtype ndarray:
        """

        return solve(self._matrix_A, self._matrix_b)
