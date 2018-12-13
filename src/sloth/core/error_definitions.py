"""
Defines overloaded operators for basic mathematical operations over unit-containing members (Constant, Parameter, Variables)
"""

class ExposedVariableError(Exception):

    """
    Error raised by the utilization of non-exposed variables for connection of two Model objects.
    """

    def __init__(self, model_1_exposed_vars, model_2_exposed_vars, output_var, input_var):

        self.m1_exposed_names = [var_i.name for var_i in model_1_exposed_vars]

        self.m2_exposed_names = [var_i.name for var_i in model_2_exposed_vars]

        self.input_var_name = input_var.name

        self.output_var_name = output_var.name

    def __str__(self):

        msg = "Non-exposed variable declaration in the output model(1) \n %s \n and/or input model(2) \n %s. \n The declared output variable name is %s, and the input variable name is %s." % (self.m1_exposed_names, self.m2_exposed_names, self.output_var_name, self.input_var_name)

        return(msg)

class UnexpectedObjectDeclarationError(Exception):

    """
    Error raised by the utilization of a non-registered Variable, Parameter or Constant for the current Model.
    """

    def __init__(self, objects, declared_objects):

        self.objects = objects

        self.declared_objects = declared_objects

    def __str__(self):

        msg = "Unexpected object declaration error. \n The following objects were used: %s \n But the following objects were declared for the current model. \n %s" % (self.objects, self.declared_objects)

        return(msg)


class AbsentRequiredObjectError(Exception):

    """
    Error raised by the absence of an required object.
    """

    def __init__(self, expected_type):

        self.expected_type = expected_type

    def __str__(self):

        msg = "Absent required object error. A %s was expected, but no one was supplied." % (self.expected_type)

        return(msg)


class UnexpectedValueError(Exception):

    """
    Error raised by input of an unexpected value.
    """

    def __init__(self, expected_type):

        self.expected_type = expected_type

    def __str__(self):

        msg = "Unexpected value error. A %s was expected, but one divergent type was supplied." % (self.expected_type)

        return(msg)


class UnresolvedPanicError(Exception):

    """
    Error raised by unresolved problems. Ideally this exception would never arises. It is included only for debugging purposes
    """

    def __init__(self):

        pass

    def __str__(self):

        msg = "Unresolved Panic Error. This should not have ocurrred. \n Perhaps you should debug your code."

        return(msg)



class NonDimensionalArgumentError(Exception):

    """
    Error raised when a non-dimensional argument was expected but a dimensional one was provided.
    Typically occurs in transcendental functions (log, log10, sin, cos, etc...)
    """

    def __init__(self, unit):

        self.unit = unit

    def __str__(self):

        msg = "A dimensionless argument was expected \n" + \
              str(self.unit.dimension)

        return(msg)

class DimensionalCoherenceError(Exception):

    """
    Error raised when two non-coherent dimensions are summed or subtracted
    """
    def __init__(self, unit_1, unit_2):

        if unit_1 == None:
            self.unit_1 = {'m':0.0,'kg':0.0,'s':0.0,'A':0.0,'K':0.0,'mol':0.0,'cd':0.0}
        else:
            self.unit_1 = unit_1

        if unit_2 == None:
            self.unit_2 = {'m':0.0,'kg':0.0,'s':0.0,'A':0.0,'K':0.0,'mol':0.0,'cd':0.0}
        else:
            self.unit_2 = unit_2

    def __str__(self):

        msg = "Dimensions are incoherent \n(" + \
               str(self.unit_1.dimension)   + \
               "\n != \n"                       + \
               str(self.unit_2.dimension)   + \
               ")."

        return(msg)


def _addUnitContainingOperations(a,b):

    return(a._checkDimensionalCoherence(b))
   