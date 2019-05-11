# *coding:utf-8*

"""
Define Model class, for storage of equations, distribution on domains and information about input and output variables (exposed variables), and incorporation of other models variables and equations
"""
import collections
from .core.error_definitions import UnexpectedObjectDeclarationError, UnexpectedValueError
from .core.equation import Equation
from .core.equation_operators import Log, Log10, Sqrt, Abs, Exp, Sin, Cos, Tan
from .core.variable import Variable
from .core.constant import Constant
from .core.parameter import Parameter
from . import analysis
from . import connection
import prettytable

from copy import deepcopy

class Model:

    """
    Model class definition. Stores several Equation objects, map exposed the exposed variables of the model and allow distribution of a variable among a specific domain.

    * Note:

        Mandatory structure that user should supply when importing Model:

        * DeclareVariables()
            Function  that is executed in the initial preparation of the model, declaring all the Variable objects for later reference.

        * DeclareExposedVariables()
            Function for setting already defined variables as 'input' or 'output'.

        * DeclareParameters()
            Likewise DeclareVariables(), this function is used in the initial preparation of the model, declaring the Parameter objects.

        * DeclareConstants()
            By now, you shall have got the idea ;)

        *DeclareEquations()
            Function for declaration of the Equations. Later, a sanity check (method .performSanityCheck) is performed examinating all the declared Variables, Parameters, Constants and checking if those was declared.


    """

    def __init__(self, name, description = "", property_package=None):

        """
        Instantiate Model.

        :ivar str name:
            Name for the current model. Must be unanbigous to other models

        :ivar str description"
            Short description of the current model

        :ivar PropertyPackage property_package:
            Object that holds the properties (eg: physico-chemical properties, etc) for the current model. Defaults to None
        """

        self.name = name

        self.description = description

        self.property_package = property_package

        #If those argurments already exists due to model inheritance:

        try:

            len(self.exposed_vars) #Check if it already was defined
        except:
            self.exposed_vars = {'input':[], 'output':[]} #Nope. Define it

        try:
            len(self.parameters)
        except:
            self.parameters = {}#collections.OrderedDict({})

        try:
            len(self.variables)
        except:
            self.variables = {}#collections.OrderedDict({})

        try:
            len(self.constants)
        except:
            self.constants = {}#collections.OrderedDict({})

        try:
            len(self.equations)
        except:
            self.equations = {}#collections.OrderedDict({})

        try:
            len(self.connections)
        except:
            self.connections = {}#collections.OrderedDict({})

        self.objects_info = {}

        self.ignore_equation_warning = False

        self.ignore_variable_warning = False

    def _gatherObjectsInfo_(self):

        """
        Function for gathering information about the name of all declared objects for the current model.
        """

        self.objects_info = {}

        self.objects_info[ 'equations' ] = list(self.equations.keys())

        self.objects_info[ 'constants' ] = list(self.constants.keys())

        self.objects_info[ 'parameters' ] = list(self.parameters.keys())

        self.objects_info[ 'variables' ] = list(self.variables.keys())

        self.objects_info[ 'connections' ] = list(self.connections.keys())

        self.objects_info[ 'exposed_vars' ] = self.exposed_vars

    def _getModelOverviewForGraph(self):

        input_var_names, output_var_names = self._infoInputOutputVariables(False)

        self._gatherObjectsInfo_()

        parameter_names = self.objects_info['parameters']

        return self.name+"\n\n ->input: " + ", ".join(input_var_names) + \
                        "\n\n ->output: " + ", ".join(output_var_names) + \
                        "\n\n ->parameters: " + ", ".join(parameter_names)

    def _infoInputOutputVariables(self, print_output=True):

        """
        Return information about the name of variables exposed as input and output for the current model

        :param bool print_output:
            Whether the function should print to stdout the output information or not

        :return:
            Name of input variables, name of output variables

        :rtype tuple(list(str), list(str))
        """



        input_var_names = [i_var.name for i_var in self.exposed_vars['input']]

        output_var_names = [o_var.name for o_var in self.exposed_vars['output']]

        if print_output is True:

            print("\nModel: {}\n\tInput var. names: {}\n\tOutput var. names:{}".format(self.name, input_var_names, output_var_names))

        return input_var_names, output_var_names

    def _infoModelReport_(self):

        print(analysis.Analysis().modelReport(self))

    def _infoDegreesOfFreedom_(self):

        """
        Return information about the number of degrees of freedom

        :return:
            Number of design, control and chemical degrees of freedom.
        :rtype:
            tuple (int,int,int)
        """

        rtrn_tab = prettytable.PrettyTable()

        rtrn_tab.field_names = ['Nb. Equations','Nb. Variables', 'Nb. Parameters']
        rtrn_tab.add_row([ str(len(self.equations)), \
                              str(len(self.variables)) , \
                              str(len(self.parameters))
                            ])
        print(rtrn_tab)

        rtrn_tab = prettytable.PrettyTable()

        rtrn_tab.field_names = ['Nb. Components','Nb. Phases']
        rtrn_tab.add_row([ str(0), str(0) ])

        print(rtrn_tab)


        rtrn_tab = prettytable.PrettyTable()

        rtrn_tab.field_names = ['Nb. M.V.']
        rtrn_tab.add_row([ str(0)])

        print(rtrn_tab)

        df_design = len(self.equations) - (len(self.variables) + len(self.parameters))

        df_control = 0

        df_chemical = 0

        rtrn_tab = prettytable.PrettyTable()

        rtrn_tab.field_names = ['Nb. DF. Design','Nb. DF. Control', 'Nb. DF. Chemical']
        rtrn_tab.add_row([ str(df_design), str(df_control), str(df_chemical) ])

        print(rtrn_tab)


        return(df_design, df_control, df_chemical)

    def _checkEquation_(self, eq):

        #Check if all objects used in the current equation were declared

        all_objects_keys = list(self.variables.keys())  + \
                           list(self.parameters.keys()) + \
                           list(self.constants.keys())

        is_declared = all( obj_i in all_objects_keys for obj_i in list(eq.objects_declared.keys()) )

        if is_declared != True:

            self._gatherObjectsInfo_()

            raise (UnexpectedObjectDeclarationError( list(eq.objects_declared.keys()), self.objects_info ))

            return(False)

        else:

            return(True)

    def __call__(self):

        """
        Overloaded function used to resolve all the configurations necessary for model definition, such as equation, variable, parameters and constant declarations, etc
        """

        self.DeclareConstants()

        self.DeclareParameters()

        self.DeclareVariables()

        self.DeclareEquations()

        if len(self.variables) == 0 and self.ignore_variable_warning is False:

            print("Warning: No variables were declared.")

        if len(self.equations) == 0 and self.ignore_equation_warning is False:

            print("Warning: No equations were declared.")

    def _createConnection(self, name, description, out_vars, in_vars, out_model, expr):

        """
        Function for creation of an Connection object, and inclusion of a connective equation in the current model. Typically called externally.

        :ivar str name:
            Name for the current equation

        :ivar str description:
            Description for the present equation. Defaults to ""

        :param list(Variable) out_vars:
            List of Variable objects from which that supplies the input object

        :param list(Variable) in_vars:
            List of Variable objects that is supplied by the output object

        :param List(Variable) out_model_exposed_vars:
            List of exposed variables of 'output' type in the output Model

        :param list(EquationNode) expr:
            List of EquationNode objects to declare for the current Equation object.
        """


        in_vars_is_Var = all(isinstance(in_i, Variable) for in_i in in_vars)

        out_vars_is_Var = all(isinstance(out_i, Variable) for out_i in out_vars)

        if in_vars_is_Var and out_vars_is_Var:

            out_vars_names = (",").join([out_i.name for out_i in out_vars])

            in_vars_names = (",").join([in_i.name for in_i in in_vars])

            name = out_vars_names+"--->"+in_vars_names

            description = "["+out_vars_names+"--->"+in_vars_names+"]"

            conn = connection.Connection(name, description, in_vars_names, out_vars_names, expr)

            conn.setResidual(expr) # I DON'T UNDERSTAND WHY THIS NEED TO BE HERE! x)

            conn._sweepObjects()

            self.equations[name] = conn

            return(conn)

        else:

            raise UnexpectedValueError("list(Variable)")


    def _ownObjectFromModel(self, obj, model):

        """
        Function for copying an object from another model and changing its ownership (eg:_<MODEL_NAME> name convention)
        """

        print("\n\t Re-owning object ",obj.name, "fom model ",model.name)

        obj_ = deepcopy(obj)

        obj_.name = obj.name[:-(1+len(model.name))] +'_'+self.name

        print("\n\t\t Re-naming object fom ",obj.name, "to ", obj_.name)

        print("\n\t\t Its new __dict__ is: ",obj_.__dict__)

        return(obj_)


    def _incorporateFromModel(self, model, copy_objects=True, register_variables=True, register_parameters=True, register_constants=True, register_equations=True, register_connections=True, print_debug_msg=False):

        """
        Function for incorporation of another model in the current one, copying its variables, parameters, equations, etc.

        :ivar model:
            Model form which desired objects should be incorporated

        :param bool copy_objects:
            If the atributes of the python object should be copied, allowign them to be acessed directly in the current Model object as if they were declared natively (eg:equation definition)

        :param bool register_variables:
            If the variables should be copied from the donor model to the one that will incorporate. Defaults to True.

        :param bool register_parameters:
            If the parameters should be copied from the donor model to the one that will incorporate. Defaults to True.

        :param bool register_constants:
            If the constants should be copied from the donor model to the one that will incorporate. Defaults to True.

        :param bool register_equations:
            If the equations should be copied from the donor model to the one that will incorporate. Defaults to True.

        :param bool registerister_connections:
            If the connections should be copied from the donor model to the one that will incorporate. Defaults to True.
        """

        if print_debug_msg is True:
            print("==> Copying directly objects from model ", model.name,": ")

        if copy_objects is True:

            #Copy atributes from donor model as if they were declared natively for the current one

            fixed_elements = ['variables', 'parameters', 'constants', 'equations', 'name', 'description', 'property_package', 'exposed_vars', 'connections', 'objects_info', 'ignore_equation_warning', 'ignore_variable_warning']

            self.__dict__.update( { k: self._ownObjectFromModel(model.__dict__[k], model) for k in model.__dict__.keys() if k not in fixed_elements } )

            if print_debug_msg is True:
                print("\n ==>Registering objects from donor model dictionaries")

        if register_variables is True:

            if print_debug_msg is True:
                print("\n \t\t Old variables dict for current model: ", self.variables)

            _ = [ self._registerVariableDirectly(var_i[1], model) for var_i in list(model.variables.items()) ]

            if print_debug_msg is True:
                print("\n \t\t New variables dict for current model: ", self.variables)

        if register_parameters is True:

            if print_debug_msg is True:
                print("\n \t\t Old parameters dict for current model: ", self.parameters)

            _ = [ self._registerParameterDirectly(par_i[1], model) for par_i in list(model.parameters.items()) ]

            if print_debug_msg is True:
                print("\n \t\t New parameters dict for current model: ", self.parameters)

        if register_constants is True:

            if print_debug_msg is True:
                print("\n \t\t Old constants dict for current model: ", self.constants)

            _ = [ self._registerParameterDirectly(con_i[1], model) for con_i in list(model.constants.items()) ]

            if print_debug_msg is True:
                print("\n \t\t New constants dict for current model: ", self.constants)

        if register_equations is True:

            if print_debug_msg is True:
                print("\n \t\t Old equations dict for current model: ", self.equations)

            _ = [ self._registerEquationDirectly(eq_i[1], model) for eq_i in list(model.equations.items()) ]

            if print_debug_msg is True:
                print("\n \t\t New equations dict for current model: ", self.equations)

        if print_debug_msg is True:
            print("\n==>New __dict__ for current object is: ", self.__dict__)

    def _registerVariableDirectly(self, var, model_to_incorporate):

        """
        Create a Variable object directly, and register it. Intended only for internal use when incorporating other models

        :ivar var:
            Variable object that will be registered in the current Model object

        :ivar model_to_incorporate:
            Model from which the object will be incorporated
        """

        print ("")

        var = deepcopy(var)

        var.name = var.name[:-(1+len(model_to_incorporate.name))] +'_'+self.name

        self.variables[var.name] = var

        if var.is_exposed == True:

            type = var.type

            self.exposed_vars[type].append(var)

    def _registerParameterDirectly(self, par, model_to_incorporate):

        """
        Create a Parameter object directly, and register it. Intended only for internal use when incorporating other models

        :ivar par:
            Parameter object that will be registered in the current Model object

        :ivar model_to_incorporate:
            Model from which the object will be incorporated
        """

        par = deepcopy(par)

        par.name = par.name[:-(1+len(model_to_incorporate.name))] +'_'+self.name

        self.parameters[par.name] = par

    def _registerConstantDirectly(self, con, model_to_incorporate):

        """
        Create a Constant object directly, and register it. Intended only for internal use when incorporating other models

        :ivar con:
            Constant object that will be registered in the current Model object

        :ivar model_to_incorporate:
            Model from which the object will be incorporated
        """

        con = deepcopy(con)

        con.name = con.name[:-(1+len(model_to_incorporate.name))] +'_'+self.name

        self.constants[con.name] = con

    def _registerEquationDirectly(self, eq, model_to_incorporate):

        """
        Create a Equation object directly, and register it. Intended only for internal use when incorporating other models

        :ivar eq:
            Equation object that will be registered in the current Model object

        :ivar model_to_incorporate:
            Model from which the object will be incorporated
        """

        eq = deepcopy(eq)

        eq.name = eq.name[:-(1+len(model_to_incorporate.name))] +'_'+self.name

        eq._sweepObjects()

        self.equations[eq.name] = eq


    def createVariable(self, name, units , description = "", is_lower_bounded = False, is_upper_bounded = False, lower_bound = None, upper_bound = None, is_exposed = False, type = '', latex_text="", value = 0.):

        """

        Function for creation of an Variable object. Store an Variable object in '.variables' dict. Mandatory interface for model Variable creation in the DeclareVariables() function.

        :param str name:
        Name for the current variable

        :param Unit units:
        Definition of dimensional unit of current variable

        :param str description:
        Description for the present variable. Defauls to ""

        :param bool isLowerBounded:
        Define if the Variable object has some minimum value restriction.
        A sanity check is performed and if lowerBound != None, isLowerBounded = True.

        :param bool isUpperBounded:
        Define if the Variable object has some maximum value restriction.
        A sanity check is performed and if upperBound != None, isUpperBounded = True.

        :param float lowerBound:
        Minimum value for Variable object

        :param float upperBound:
        Minimum value for Variable object

        :param str latex_text:
        Latex text to represent the variable

        :param float value:
        Value of the current variable. Defaults to 0.

        """

        var = Variable(name, units , description, is_exposed, type, is_lower_bounded, is_upper_bounded, lower_bound, upper_bound, value, latex_text)

        var.name=var.name+'_'+self.name

        self.variables[var.name] = var

        if is_exposed == True:

            self.exposed_vars[type].append(var)

        return var

    def createParameter(self, name, units , description = "", value = 0, latex_text=""):

        """

        Function for creation of an Parameter object. Store an Parameter object in '.Parameters' dict. Mandatory interface for model Parameter creation in the DeclareParameters() function.

        :param str name:
        Name for the current Parameter

        :param Unit units:
        Definition of dimensional unit of current Parameter

        :param str description:
        Description for the present Parameter. Defauls to ""

        :param float value:
        Value of the current Parameter. Defaults to 0.

        :param str latex_text:
        Latex text to represent the parameter
        """
        par = Parameter(name, units , description, value, latex_text)

        par.name=par.name+'_'+self.name

        self.parameters[par.name] = par

        return par

    def createConstant(self, name, units , description = "", value = 0, latex_text=""):

        """

        Function for creation of an Constant object. Mandatory interface for model Constant creation in the DeclareConstants() function.

        :param str name:
        Name for the current Constant

        :param Unit units:
        Definition of dimensional unit of current Constant

        :param str description:
        Description for the present constant. Defauls to ""

        :param float value:
        Value of the current constant. Defaults to 0.

        :param str latex_text:
        Latex text to represent the constant
        """

        con = Constant(name, units , description, value, latex_text)

        con.name=con.name+'_'+self.name

        self.constants[con.name] = con

        return con


    def createEquation(self, name, description="", expr=None, check_equation=True):

        """
        Function for creation of an Equation object. Mandatory interface for model equation creation in the specific declaratory section.

        :ivar str name:
            Name for the current equation

        :ivar str description:
            Description for the present equation. Defaults to ""

        :param EquationNode expr:
            EquationNode object to declare for the current Equation object. Defaults to None
        """

        eq = Equation(name, description, expr)
        eq.setResidual(expr) # I DON'T UNDERSTAND WHY THIS NEED TO BE HERE! x)

        eq.name=eq.name+'_'+self.name

        # #\nCreating equation for expression: %s\n     And its symbolic map is: %s"%(eq.equation_expression, eq.equation_expression.repr_symbolic, eq.equation_expression.symbolic_map))

        # print("\n==FOR EQUATION== \nEquation expression: %s"%(eq.equation_expression))

        eq._sweepObjects()

        #Check if all objects used in the current equation were declared

        if check_equation is True:

            if self._checkEquation_(eq) is True:

                self.equations[eq.name] = eq

                return eq

            else:

                pass

        else:

            self.equations[eq.name] = eq

            return eq


    #==== FUNCTIONS THAT SHOULD BE PROVIDED BY THE USER ====

    def DeclareVariables(self):

        pass

    def DeclareParameters(self):

        pass

    def DeclareConstants(self):

        pass

    def DeclareEquations(self):

        pass
    #=======================================================
