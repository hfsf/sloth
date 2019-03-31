# *coding:utf-8*

"""
Define Problem class. Unite several Model classes through Connections, forming one single Equation block. Used by Simulation class to perform the calculations.
"""

from .core.error_definitions import ExposedVariableError, AbsentRequiredObjectError
from .core.equation_block import EquationBlock
from collections import OrderedDict
from .core.variable import Variable
from .core.parameter import Parameter
import numpy as np

class Problem:

    """
    Problem class definitions. Unite several Model objects into one single equation block for solving.
    """

    def __init__(self, name, description="", models={}, connections={}, variable_dict={}, parameter_dict={}):

        """
        Instantiate Problem.

        :ivar str name:
            Name for the current problem

        :ivar str description:
            Description of the current problem
        """

        self.name = name

        self.description = description

        self.models = OrderedDict(models)

        self.connections = OrderedDict(connections)

        self._equation_list = None

        self.equation_block = None

        self.initial_conditions = {}

        self.variable_dict = OrderedDict(variable_dict)

        self.parameter_dict = OrderedDict(parameter_dict)

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

        _param_dict = {}

        _param_list = []

        _param_name_list = []


        for model_i in list(self.models.values()):

            for eq_i in list(model_i.equations.values()):

                self._equation_list.append(eq_i)

                for obj_i in list(eq_i.objects_declared.values()):

                    if obj_i not in _var_list and isinstance(obj_i, Variable):

                        _var_dict[obj_i.name] = obj_i

                        _var_list.append(obj_i)

                        _var_name_list.append(obj_i.name)

                    elif obj_i not in _param_list and isinstance(obj_i, Parameter):

                        _param_dict[obj_i.name] = obj_i

                        _param_list.append(obj_i)

                        _param_name_list.append(obj_i.name)

        #=================================================================

        #Remove unused variables from self.variable_dict and self.param_dict

        variable_dict_ = OrderedDict({})

        _ = [variable_dict_.update({k:self.variable_dict[k]}) for k in self.variable_dict.keys() if k in _var_name_list]

        parameter_dict_ = OrderedDict({})

        _ = [parameter_dict_.update({k:self.parameter_dict[k]}) for k in self.parameter_dict.keys() if k in _param_name_list]

        self.equation_block = EquationBlock(equations=self._equation_list, variable_dict=variable_dict_, parameter_dict=parameter_dict_)

    def createConnection(self, model_1, model_2, output_vars, input_vars, expr=None, description=""):

        """
        Connect two Models creating a Connection for both models, linking the ouput variable of the former to the input variable of the later.
        """

        if isinstance(input_vars, list):

            input_var_is_declared= all(in_i in model_2.exposed_vars['input'] for in_i in input_vars)

        else:

            input_var_is_declared= input_vars in model_2.exposed_vars['input']

        if isinstance(output_vars, list):

            output_var_is_declared= all(out_i in model_1.exposed_vars['output'] for out_i in output_vars)

        else:

            output_var_is_declared= output_vars in model_1.exposed_vars['output']

        if output_var_is_declared and input_var_is_declared:

           # Creating connection equation in the second Model object

           #return self._createDirectConnection(model_1, output_var, model_2, input_var)


            if not isinstance(output_vars, list):

                output_var_ = [output_vars]

            else:

                output_var_ = output_vars

            if not isinstance(input_vars, list):

                input_var_ = [input_vars]

            else:

                input_var_ = input_vars

            if expr is None:

                expr = sum([in_var_i.__call__() for in_var_i in input_var_]) - sum([out_var_i.__call__() for out_var_i in output_var_])

            # The process of connection creation

            self._createDirectConnection(model_1, output_var_, model_2, input_var_, expr, description)

        else:

            raise ExposedVariableError(model_1.exposed_vars['output'], model_2.exposed_vars['input'], output_vars, input_vars) 


    def _createDirectConnection(self, out_model, out_vars, in_model, in_vars, expr, description):

        """
        Create a connection beetween one model an their output variable, and another model and other variable, which is an input for the later model
        """

        out_var_names = (",").join([out_i.name for out_i in out_vars])

        in_var_names = (",").join([in_i.name for in_i in in_vars])

        conn = in_model._createConnection(out_var_names+"--->"+in_var_names, description, out_vars, in_vars, out_model, expr)

        #in_model._createConnection(out_var.name+"--->"+in_var.name, description, out_var, in_var, out_model, expr)

        self.connections[out_var_names+"@"+out_model.name+" ---> "+in_var_names+"@"+in_model.name] = conn

        #return conn

    def _reloadModels(self, models_name=None):

        """
        Reload defined models, redefining their equations
        """

        if models_name is None:

            _ = [mod_i() for mod_i in self.models.values()]

        else:

            _ = [mod_i() for mod_i in self.models.values() if mod_i.name in models_name]

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

            self.parameter_dict.update(model_list.parameters)

    def resolve(self):

        """
        Resolve current Problem object, builing its EquationBlock object and resolving it
        """ 
    
        self._reloadModels()

        self._buildEquationBlock()

        self.equation_block()
