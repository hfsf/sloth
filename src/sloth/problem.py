# *coding:utf-8*

"""
Define Problem class. Unite several Model classes through Connections, forming one single Equation block. Used by Simulation class to perform the calculations.
"""

from .core.error_definitions import ExposedVariableError
from .core.equation_block import EquationBlock
from collections import OrderedDict
from .core.variable import Variable
import numpy as np

class Problem:

    """
    Problem class definitions. Unite several Model objects into one single equation block for solving.
    """

    def __init__(self, name, description=""):

        """
        Instantiate Problem.

        :ivar str name:
            Name for the current problem

        :ivar str description:
            Description of the current problem
        """

        self.name = name

        self.description = description

        self.models = OrderedDict({})

        self.connections = OrderedDict({})

        self._equation_list = None

        self.equation_block = None

        self.initial_conditions = {}

        self.variable_dict = OrderedDict({})

    def setInitialConditions(self, condition):

        """
        Set initial condition for ODE and DAE systems.

        :param dict condition:
            Dictionary containing the initial condition for each Variable object that is differentiated
        """

        self.initial_conditions.update(condition)

    def _getProblemType(self):

        is_linear = len(self.equation_block._equation_groups['linear']) > 0

        is_nonlinear = len(self.equation_block._equation_groups['nonlinear']) > 0

        is_differential = len(self.equation_block._equation_groups['differential']) > 0

        # Check if the problem is D (strictly Differential), DAE (differential + linear or nonlinear), NLA (nonlinear) or LA (linear)

        is_D = is_differential==True and (is_linear==False and is_nonlinear==False)
        is_DAE = is_differential==True and (is_linear==True or is_nonlinear==True)
        is_NLA = is_differential==False and (is_nonlinear==True)
        is_LA = is_differential==False and (is_nonlinear==False and is_linear==True)

        if is_D:

            return "differential"

        elif is_DAE:

            return "differential-algebraic"

        elif is_NLA:

            return "nonlinear"

        elif is_LA:

            return "linear"

        else:

            return None

    def _buildEquationBlock(self):

        """
        Return the EquationBlock object for the models defined for the current problem.
        """

        #eqs_ = [ list(model_i.equations.values()) for model_i in self.models.values() ]

        #self._equation_list = (np.array(eqs_).ravel()).tolist()

        #================== OPTIMIZE THIS CODE SNIPPET ===================

        self._equation_list = []

        _var_dict = {}

        _var_list = []

        _var_name_list = []

        for model_i in list(self.models.values()):

            for eq_i in list(model_i.equations.values()):

                self._equation_list.append(eq_i)

                for var_i in list(eq_i.objects_declared.values()):

                    if var_i not in _var_list and isinstance(var_i, Variable):

                        _var_dict[var_i.name] = var_i

                        _var_list.append(var_i)

                        _var_name_list.append(var_i.name)

        #=================================================================

        #Remove unused variables from self.variable_dict

        variable_dict_ = OrderedDict({})

        _ = [variable_dict_.update({k:self.variable_dict[k]}) for k in self.variable_dict.keys() if k in _var_name_list]

        self.equation_block = EquationBlock(equations=self._equation_list, variable_dict=variable_dict_)

    def createConnection(self, model_1, model_2, output_var, input_var, expr=None):

        """
        Connect two Models creating a Connection for both models, linking the ouput variable of the former to the input variable of the later.
        """

        if output_var in model_1.exposed_vars['output'] and \
           input_var  in model_2.exposed_vars['input']:

           # Creating connection equation in the second Model object

           conn = model_2._createConnection("","", output_var, input_var, \
                                            model_1, expr)

           self.connections[output_var.name+"@"+model_1.name+" ---> "+input_var.name+"@"+model_2.name] = conn

           return conn

        else:

            raise ExposedVariableError(model_1.exposed_vars['output'], model_2.exposed_vars['input'], output_var, input_var) 

    def addModels(self, model_list):

        """
        Add models to current problem

        :param [Model, list(Model)] mod_list:
            Model to be added to the current Problem.
        """
        
        if isinstance(model_list,list):

            # A list of models were supplied

            #self.models = OrderedDict( (modx.name,modx) for modx in model_list )

            _ = [self.addModels(modx) for modx in model_list]

        else:

            # A single model was supplied

            self.models[model_list.name] = model_list

            self.variable_dict.update(model_list.variables)

    def resolve(self):

        """
        Resolve current Problem object, builing its EquationBlock object and resolving it
        """ 
    
        self._buildEquationBlock()

        self.equation_block()
