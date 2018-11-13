# *coding:utf-8*

"""
Defines Analysis class. The class is responsible for degrees-of-freedom (DoF) analysis, printing general information about Problem and Models.
"""

import beautifultable
import core.variable as variable
import core.constant as constant
import core.parameter as parameter

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

        var_str = [obj_i for obj_i in symb_map if isinstance(symb_map[obj_i], variable.Variable)]

        param_str = ["{}{}".format(obj_i, '(*)'*(symb_map[obj_i].is_specified==True)) for obj_i in symb_map if isinstance(symb_map[obj_i], parameter.Parameter)]

        con_str = ["{}{}".format(obj_i, '(*)'*(symb_map[obj_i].is_specified==True)) for obj_i in symb_map if isinstance(symb_map[obj_i], constant.Constant)]

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

        tab = beautifultable.BeautifulTable(max_width=120)

        tab.clear()

        # tab.column_widths = [20,30,20,15,15]

        tab.column_headers = ["Equation name","Description",
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

            tab.append_row([eq_name, eq_description, eq_repr, eq_vars, eq_params, eq_cons, eq_type])

        return(tab)