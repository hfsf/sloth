# *coding:utf-8*

"""
Define Domain class, which distributes one equation among a domain of variables.  
"""

class Domain:

    """
    Domain class definition. Distributes equations, parameters or variables within a domain of variables (currently, only unidmensional domains are supported).
    """

    def __init__(self, name, units, independent_vars={}, description="", lower_bound={'all':None}, upper_bound={'all':None}):

        """
        Instantiate Domain.

        :ivar str name:
            Name of the current domain

        :ivar Unit units:
            Dimensional information of the dependent variables on the current domain.

        :ivar dict(Variable) independent_vars:
            Dict of independent variables for the current domain. Currently only unidimensional domains are supported.

        :ivar str description:
            Description of the current domain.

        :ivar dict(Float) lower_bound:
            Inferior limit for the independent variables in which the current domain rely on, with a key for each variable or 'all' for one single value for whole domain.

        :ivar dict(Float) upper_bound:
            Superior limit for the independent variables in which the current domain rely on, with a key for each variable or 'all' for one single value for whole domain.            
        """

        self.name = name

        self.units = units

        self.independent_vars = independent_vars

        self.dependent_obj = {}

        self.description = description

        self.lower_bound = lower_bound

        self.upper_bound = upper_bound

    def __getitem__(self, idx):

        """
        
        """

        pass

    def setDomain(self, independent_vars):

        """
        Set the independent variables on which the current domain rely on. Currently only unidimensional domains are suported.

        :ivar independent_vars:
            Independent vars on which the current domain rely on. Currently only unidimensional domains are suported.
        """

        pass


    def distributeOnDomain(self, dependent_obj):

        """
        Distribute one dependent object into the current domain.

        :ivar Equation, Quantity dependent_obj:
            Dependent objects (Euquation, Variable, Parameter, Constant) that are distributed along the current domain.
        """

        pass