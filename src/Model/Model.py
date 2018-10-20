"""

Define Model class.
-Stores several equations.
-Stores one domain in which the variables are distributed.
-Stores information about input and output variables (exposed variables).

"""

from core.Equation import *
import core.Variable as Variable
import core.Constant as Constant
from DOF import curatorship

class Model(object):

    """
    
    Model class definition. Holds capabilites for:
    - Storage of several Equation objects, curating for DOF
    - Declaration of exposed variables (input, output) through Connections.

    * TODO: 
    - Include capabilities for inheriting from parent models (parent_model)

    -------------------------------------------------------------------------

    ## Mandatory structure that user should supply when importing Model:

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

    def __init__(self, name = "", description = "", parent_model = None)

        if parent_model != None: #Inherit from parent_model if it was defined.

            super(self.__class__,self).__init__(name, description)

        """

        Initial definitions.

        :param str name:
        Name for the current model

        :param str description"
        Short description of the current model

        :param Model parent_model:
        Base model fro the current, which will inherit equations, exposed variables, etc from the first.
        Defaults to 'None' (so, its a brand new model).

        """

        self.name = name

        self.description = description

        self.parent_model = parent_model

        if parent_model == None:

            self.exposed_vars = {'input':[],'output':[]}

        self.parameters = {}

        self.variables = {}

        self.equations = {}

    def __call__(self):

        """

        Overloaded function used to resolve all the configurations necessary for model definition, such as equation, variable, parameters and constant declarations, etc

        """

        self.DeclareConstants()

        self.DeclareParameters()

        self.DeclareVariables()

        self.DeclareEquations()

        self.DeclareExposedVariables()

        self.DeclareConnections()

        if len(self.variables) == 0:

            print "Warning: No variables were declared."

        if len(self.equations) == 0:

            print "Warning: No equations were declared."

    def createEquation(self, name, description, fast_expr = None):

        """
        
        Function for creation of an Equation object. Store an Equation object in '.equations' dict. Mandatory interface for model equation creation in the DeclareEquations() function.

        :param str name:
        Name for the current equation

        :param str description:
        Description for the present equation. Defauls to ""

        :param ExpressionTree fast_expr:
        ExpressionTree object to declare for the current Equation object.  If declared, the moethod '.setResidual' are executed as a shortcut. Defaults to None.

        """

        eq = Equation(name, description, fast_expr)

        self.equations[eq.name] = eq

        return eq

    def createVariable(self, name, units , description = "", isLowerBounded = False, isUpperBounded = False, lowerBound = None, upperBound = None, value = 0):

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

        var = Variable.Variable(name, units , description, isLowerBounded, isUpperBounded, lowerBound, upperBound, value)

        self.variables[var.name] = var

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

        par = Parameter.Parameter(name, units , description, value)

        self.parameters[par.name] = par

        return par


    def createConstant(self, name, units , description = "", value = 0):

        """
        
        Function for creation of an Constant object. Optional interface for model Constant creation in the DeclareConstants() function.

        :param str name:
        Name for the current Constant

        :param Unit units:
        Definition of dimensional unit of current Constant

        :param str description:
        Description for the present Constant. Defauls to ""

        :param float value:
        Value of the current Constant. Defaults to 0.      

        """

        con = Constant.Constant(name, units , description, value)

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

    def DeclareExposedVariables(self):

        pass

    def DeclareConnections(self):

        pass
    #=======================================================