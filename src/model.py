# *coding:utf-8*

"""
Define Model class, for storage of equations, distribution on domains and information about input and output variables (exposed variables).
"""

import core.error_definitions as errors  
from core.equation import *
from core.equation_operators import *
import core.variable as variable
import core.constant as constant
import core.parameter as parameter
import connection
import beautifultable

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

        * DeclareConnections()
            Function for declaration of the Connections. Those special equations are used to receive external input (eg: output from another model, external input for the current process, etc) and provide output (eg: input to another model, or simple output for the current process).

    """

    def __init__(self, name = "", description = "", parent_model = None):

        if parent_model != None: 

            # Inherit from parent_model if it was defined.

            super().__init__(name, description)

        """
        Instantiate Model.

        :ivar str name:
            Name for the current model

        :ivar str description"
            Short description of the current model

        :param Model parent_model:
            Base model fro the current, which will inherit equations, exposed variables, etc from the first. Defaults to None
        """

        self.name = name

        self.description = description

        self.parent_model = parent_model

        if parent_model == None:

            self.exposed_vars = {'input':[], 'output':[]}

        self.parameters = {}

        self.variables = {}

        self.constants = {}

        self.equations = {}

        self.connections = {}

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

    def _infoDegreesOfFreedom_(self):

        """
        Return information about the number of degrees of freedom
        
        :return:
            Number of design, control and chemical degrees of freedom.
        :rtype:
            tuple (int,int,int)
        """

        rtrn_tab = beautifultable.BeautifulTable()

        rtrn_tab.column_headers = ['Nb. Equations','Nb. Variables', 'Nb. Parameters']
        rtrn_tab.append_row([ str(len(self.equations)), \
                              str(len(self.variables)) , \
                              str(len(self.parameters))
                            ])
        print(rtrn_tab)

        rtrn_tab = beautifultable.BeautifulTable()

        rtrn_tab.column_headers = ['Nb. Components','Nb. Phases']
        rtrn_tab.append_row([ str(0), str(0) ])

        print(rtrn_tab)


        rtrn_tab = beautifultable.BeautifulTable()

        rtrn_tab.column_headers = ['Nb. M.V.']
        rtrn_tab.append_row([ str(0)])

        print(rtrn_tab)

        df_design = len(self.equations) - (len(self.variables) + len(self.parameters))

        df_control = 0

        df_chemical = 0

        rtrn_tab = beautifultable.BeautifulTable()

        rtrn_tab.column_headers = ['Nb. DF. Design','Nb. DF. Control', 'Nb. DF. Chemical']
        rtrn_tab.append_row([ str(df_design), str(df_control), str(df_chemical) ])

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

            raise (errors.UnexpectedObjectDeclarationError( list(eq.objects_declared.keys()), self.objects_info ))

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

        self.DeclareConnections()

        if len(self.variables) == 0:

            print("Warning: No variables were declared.")

        if len(self.equations) == 0:

            print("Warning: No equations were declared.")

    def _createConnection(self, name, description, out_var, in_var, out_model, expr=None):

        """
        Function for creation of an Connection object, and inclusion of a connective equation in the current model. Typically called externally.
        
        :ivar str name:
            Name for the current equation

        :ivar str description:
            Description for the present equation. Defaults to ""

        :param Variable out_var:
            Variable object from which that supplies the input object

        :param Variable in_var:
            Variable object that is supplied by the output object

        :param List(Variable) out_model_exposed_vars:
            List of exposed variables of 'output' type in the output Model

        :param EquationNode expr:
            EquationNode object to declare for the current Equation object. Defaults to None
        """

        if isinstance(in_var, variable.Variable) and isinstance(out_var, variable.Variable):


            if in_var in self.exposed_vars['input'] and \
               out_var in out_model.exposed_vars['output']:

                name = out_var.name+"--->"+in_var.name

                description = "Connection from "+out_model.name+" ("+out_var.name+"--->"+in_var.name+")"

                if expr == None:

                    expr = in_var.__call__() - out_var.__call__()

                conn = connection.Connection(name, description, in_var.name, out_var.name, expr)

                self.equations[name] = conn

                return(conn)

            else:

                raise errors.ExposedVariableError(out_model.exposed_vars['output'], self.exposed_vars['input'], out_var, in_var)

        else:

            raise errors.UnexpectedValueError("Variable")


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

        eq._sweepObjects()

        #Check if all objects used in the current equation were declared

        if self._checkEquation_(eq) == True:
            
            self.equations[eq.name] = eq

            return eq

        else:

            pass

    def createVariable(self, name, units , description = "", is_lower_bounded = False, is_upper_bounded = False, lower_bound = None, upper_bound = None, is_exposed = False, type = '', value = 0.):

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

        :param float value:
        Value of the current variable. Defaults to 0.      

        """

        var = variable.Variable(name, units , description, is_lower_bounded, is_upper_bounded, lower_bound, upper_bound, value)

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

        par = parameter.Parameter(name, units , description, value)

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

        con = constant.Constant(name, units , description, value)

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