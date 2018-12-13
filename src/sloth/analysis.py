# *coding:utf-8*

"""
Defines Analysis class. The class is responsible for  printing general information about Problem and Models.

Defines DOF_Analysis class. This class is responsible for degrees-of-freedom (DoF) analysisis, avoiding ill-conditioned systems to be executed.
"""

import prettytable
from .core.variable import Variable
from .core.constant import Constant
from .core.parameter import Parameter

class DOF_Analysis:

    """
    Degrees of freedom analysis class.
    """

    def __init__(self, problem):

        """
        Instantiate DOF_Analysis

        :ivar Problem problem:
            Problem which need to be analyzed
        """

        self.problem = problem

    def _makeSanityChecks(self):

        assert self._dofTest(), "\n The system is ill-formed. Halt now. "

    def _dofTest(self):

        # DoF Check (Number of variables - number of equations)

        n_vars = len(self.problem.equation_block._var_list)

        n_eqs = len(self.problem.equation_block._equations_list)

        var_names_ = [i for i in self.problem.equation_block._var_list]

        n_dof = n_vars - n_eqs

        if n_vars > n_eqs:

            raise Exception("\nThe system is OVER-specified\n    Number of variables:{} ({}) \n Number of equations:{}".format(n_vars, var_names_, n_eqs))

            return False

        elif n_vars < n_eqs:

            raise Exception("\nThe system is UNDER-specified\n    Number of variables:{} Number of equations:{}".format(n_vars, n_eqs))

            return False

        else:

            # DoF == 0

            return True

class Analysis:

    """
    Analysis class definitions. Used to concentrate the information-generation methods about a Problem or a Model.
    """

    def __init__(self):

        """
        Instantiate Analysis
        """

        self.problem = None

    def _inspectForObjects(self, symb_map):

        """
        Inspect the symbolic map for variables and parameters, returing the corresponding information.

        :param dict(Quantity) symb_map:
            Dictionary for symbolic mapping of the objects used in the given EquationNode object

        :return:
            Return the formated strings corresponding to the list of Variables and Parameters objects (specified ones marked as '(*)') present in the symbolic map.

        :rtype (str,str) info:
        """

        var_str = [obj_i for obj_i in symb_map if isinstance(symb_map[obj_i], Variable)]

        param_str = ["{}{}".format(obj_i, '(*)'*(symb_map[obj_i].is_specified==True)) for obj_i in symb_map if isinstance(symb_map[obj_i], Parameter)]

        con_str = ["{}{}".format(obj_i, '(*)'*(symb_map[obj_i].is_specified==True)) for obj_i in symb_map if isinstance(symb_map[obj_i], Constant)]

        var_form = ", ".join(var_str)

        param_form = ", ".join(param_str)

        con_form = ", ".join(con_str)

        return var_form, param_form, con_form 

    def problemReport(self, problem):

        """
        Print the descritive report of the problem, using the information provided by the cointained Model objects.

        :param Problem problem:
            Problem to be examined        

        :return:
            Formated table with the information of the models
        :rtype str tabs:
        """

        tabs = ''

        for mod_i in problem.models:


            tabs += "Model: {}\n".format(mod_i) + str(self.modelReport(problem.models[mod_i]))+'\n'

        return(tabs)

    def modelReport(self, model):

        """
        Print the descritive report of the model, using the information provided by the underlying EquationNode objects.

        :param Model model:
            Model to be examined

        :return:
            Formated table with the information of the model
        :rtype str tab:
        """

        tab = prettytable.PrettyTable()

        tab.clear()

        # tab.column_widths = [20,30,20,15,15]

        tab.field_names = ["Equation name","Description",
                                "Representation","Variables",
                                "Parameters","Constants","Equation type"]

        for eq_i in model.equations:

            eq_name = model.equations[eq_i].name

            eq_description = model.equations[eq_i].description
            # Return a str with overloaded method from EquationNode class
            eq_repr = repr(model.equations[eq_i].equation_expression)

            eq_vars, eq_params, eq_cons = self._inspectForObjects(model.equations[eq_i].equation_expression.symbolic_map)

            # For a more readable output in the output table

            eq_type_pretty = {'is_linear':'linear', 'is_nonlinear':'nonlinear', 'is_differential':'differential'}

            # Search which atribute from .equation_expression.equation_type dict is True (convert set to list)

            eq_type = eq_type_pretty[ list({k for k,v in model.equations[eq_i].equation_expression.equation_type.items() if v==True})[0] ]

            tab.add_row([eq_name, eq_description, eq_repr, eq_vars, eq_params, eq_cons, eq_type])

        return(tab)