 
# *coding:utf-8*

import sympy as sp
from numpy import array as np_array
from scipy.linalg import solve
from collections import OrderedDict
from .variable import Variable

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

                if var_i not in var_list and isinstance(var_i, Variable):

                    self._var_dict[var_i.name] = var_i

                    var_list.append(var_i)

                    var_name_list.append(var_i.name)

        # ===========================================

        return var_name_list

    def _getEquationBlockAsFunction(self, differential_form='residual', side='rhs', compilation_mechanism='numpy'):
    
        """
        Return the Equations that compose the current EquationBlock object into a monolithical function that will return an array of results.

        :param str differential_form:
            Definition of which form the equations are presented, if in a 'elementary' form (y == a*x +b) or in a 'residual' form (y - a*x - b == 0). Defaults to 'residual'

        :param str side:
            Side of which the equality of the equation in the elementary form should be examined ('lhs' for left, 'rhs' for right-hand side). 

        :param str compilation_mechanism:
            Determination of which mechanism to use to compile the equations. Defaults to 'numpy'

        :return:
            Monolithic function corresponding to all the equations defined for current EquationBlock, retuning an array of results
        :rtype function:
        """
 
        # POSSIBLY UNECESSARY SNIPPET. REMOVE IN FURTHER REFACTORIES
        #===========================================================
        '''
        if differential_form == 'residual':

            symbolic_map_ = self.equations[0]._getSymbolicMap('residual')

            _ = [symbolic_map_.update(eq_i._getSymbolicMap('residual')) for eq_i in self.equations]

        if differential_form == 'elementary':

            symbolic_map_ = self.equations[0]._getSymbolicMap('elementary', side)

            _ = [symbolic_map_.update(eq_i._getSymbolicMap('elementary', side)) for eq_i in self.equations]
        '''
        #=============================================================

        fun_ = sp.lambdify(self._var_list, 
                           np_array(self._getEquationList(differential_form, side)),
                           compilation_mechanism
                    )

        return fun_

    def _getEquationList(self, differential_form=None, side='rhs'):

        """
        Set the list of sympy expressions representing the equation.

     :param str differential_form:
            Definition of which form the equations are presented, if in a 'elementary' form (y == a*x +b) or in a 'residual' form (y - a*x - b == 0). Defaults to None, for which the declared form of the equation are used.

        :param str side:
            Side of which the equality of the equation in the elementary form should be examined ('lhs' for left, 'rhs' for right-hand side). 

        :return:
            List of the sympy expressions representing each Equation object of the model

        :rtype list(sympy expresion):
        """

        #return [eq_i.equation_expression.symbolic_object for eq_i in self.equations]
        return [eq_i._getSymbolicObject(differential_form, side) for eq_i in self.equations]

    def __call__(self):

        """
        Overloaded method for EquationBlock object. Examines the equations atribute of the EquationBlock object and build the matrix 
        """

        # Fill-up the list of Variables and Equations

        self._var_list = self._getVarList()

        self._equations_list = self._getEquationList()

        self._assignEquationGroups()