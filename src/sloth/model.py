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
from . import connection
import prettytable

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

    def __init__(self, name, description = ""):

        """
        Instantiate Model.

        :ivar str name:
            Name for the current model. Must be unanbigous to other models

        :ivar str description"
            Short description of the current model

        :param Model incorporated_models:
            Base model(s) for the current, which will inherit equations, exposed variables, etc from the first. Defaults to None
        """

        self.name = name

        self.description = description

        #If those argurments already exists due to model inheritance:

        try:

            len(self.exposed_vars) #Check if it already was defined
        except:
            self.exposed_vars = {'input':[], 'output':[]} #Nope. Define it

        try:
            len(self.parameters)
        except:
            self.parameters = collections.OrderedDict({})

        try:
            len(self.variables)
        except:
            self.variables = collections.OrderedDict({})

        try:
            len(self.constants)
        except:
            self.constants = collections.OrderedDict({})

        try:
            len(self.equations)
        except:
            self.equations = collections.OrderedDict({})

        try:
            len(self.connections)
        except:
            self.connections = collections.OrderedDict({})

        self.objects_info = {}

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

    def _infoInputOutputVariables(self, return_output=True):

        """
        Return information about the name of variables exposed as input and output for the current model

        :param bool return_output:
            Whether the function should print to stdout the output information or not

        :return:
            Name of input variables, name of output variables

        :rtype tuple(list(str), list(str))
        """

        input_var_names = [i_var.name for i_var in list(self.exposed_vars['input'].items())]

        output_var_names = [o_var.name for o_var in list(self.exposed_vars['output'].items())]

        if return_output is True:

            print("\nModel: {}\n\tInput var. names: {}\n\tOutput var. names:{}".format(self.name, input_var_names, output_var_names))

        return input_var_names, output_var_names

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

        rtrn_tab.column_headers = ['Nb. Components','Nb. Phases']
        rtrn_tab.add_row([ str(0), str(0) ])

        print(rtrn_tab)


        rtrn_tab = prettytable.PrettyTable()

        rtrn_tab.column_headers = ['Nb. M.V.']
        rtrn_tab.addend_row([ str(0)])

        print(rtrn_tab)

        df_design = len(self.equations) - (len(self.variables) + len(self.parameters))

        df_control = 0

        df_chemical = 0

        rtrn_tab = prettytable.PrettyTable()

        rtrn_tab.column_headers = ['Nb. DF. Design','Nb. DF. Control', 'Nb. DF. Chemical']
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

        if len(self.variables) == 0:

            print("Warning: No variables were declared.")

        if len(self.equations) == 0:

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


    def createEquation(self, name, description="", expr=None):

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

        if self._checkEquation_(eq) == True:
            
            self.equations[eq.name] = eq

            return eq

        else:

            pass

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

        var = Variable(name, units , description, is_lower_bounded, is_upper_bounded, lower_bound, upper_bound, value, latex_text)

        var.name=var.name+'_'+self.name

        self.variables[var.name] = var

        if is_exposed == True:

            self.exposed_vars[type].append(var)

        return var

    def createParameter(self, name, units , description = "", value = 0):

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

        """
        par = Parameter(name, units , description, value)

        par.name=par.name+'_'+self.name

        self.parameters[par.name] = par

        return par

    def createConstant(self, name, units , description = "", value = 0):

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

        """

        con = Constant(name, units , description, value)

        con.name=con.name+'_'+self.name

        self.constants[con.name] = con

        return con

    #==== FUNCTIONS THAT SHOULD BE PROVIDED BY THE USER ====

    def DeclareVariables(self):

        pass

    def DeclareParameters(self):

        pass

    def DeclareConstants(self):

        pass

    def DeclareEquations(self):

        pass

    def DeclareConnections(self):

        pass
    #=======================================================
