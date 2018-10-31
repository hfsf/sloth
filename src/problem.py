"""

Define Problem class.
- Unite several Model classes through Connections, forming one single Equation block.
- Used by Simulation class to perform the calculations.

"""

class Problem(object):

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

        self.models = {}

    def addModels(self, model_list):

        """
        Add models to current problem

        :param list(Model) mod_list:
            Model to be added to the current Problem.
        """
        
        if isinstance(model_list,list):

            # A list of models were supplied

            self.models = dict( (modx.name,modx) for modx in model_list )

        else:

            # A single model was supplied

            self.models[model_list.name] = model_list
