# *coding:utf-8*

"""
Define Domain class, which distributes one equation among a domain of variables.  
"""

import pandas
from .error_definitions import UnexpectedValueError
import numpy as np
from collections import OrderedDict

class Domain:

    """
    Domain class definition. Distributes equations, parameters or variables within a domain of variables (currently, only unidmensional domains are supported), storing information.

    * TODO: Solve domain working process
    """

    def __init__(self, name, units, independent_vars=None, description="", lower_bound={'all':None}, upper_bound={'all':None}):

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

        if isinstance(independent_vars, list):

            self.independent_vars = {var.name:var for var in independent_vars}

        else:

            self.independent_vars = {}

            self.independent_vars[independent_vars.name] = independent_vars

        self.dependent_objs = OrderedDict({})

        self.description = description

        self.lower_bound = lower_bound

        self.upper_bound = upper_bound

        self.values = None

        self.is_set = False

    def __call__(self, independent_vars=None):

        """
        """

        pass

    def __getitem__(self, idx):

        """
        """

        pass

    def _setDomain(self, independent_vars=None):

        """
        Set the independent variables on which the current domain rely on. Currently only unidimensional domains are suported.

        :ivar list(Variable) independent_vars:
            Independent vars on which the current domain rely on. Currently only unidimensional domains are suported.
        """

        if self.is_set == False:

            if independent_vars == None and self.independent_vars != None:

                independent_vars = list(self.independent_vars.values())

            try:

                self.values = {var_i.name: self._createDataFramePrototype() for var_i in independent_vars}

            except:

                raise UnexpectedValueError("list(Variables)")

            self.independent_vars = independent_vars

            self.is_set = True

    def _distributeOnDomain(self, dependent_obj):

        """
        Distribute one dependent object into the current domain.

        :param Equation, Quantity dependent_obj:
            Dependent objects (Euquation, Variable, Parameter, Constant) that are distributed along the current domain.
        """

        self.dependent_objs[dependent_obj.name] = dependent_obj

    def _register(self, values, var=None):

        """
        Register values in the respective DataFrame

        :param array-like values:
            Values to register

        :param Variable var:
            Variable (independent) for which the values should be registered. Defaults to None, for which the last independent var is assumed.

        """

        if var==None:

            var = self.independent_vars

        if np.array(values).ndim == 1:

            self.values[var] = self.values[var].append(values)

    def _createDataFramePrototype(self):

        """
        Create the prototype of DataFrame for the independent variables and dependent ones

        :return data_frame_:
            Prototype of DataFrame including all the independent variables and the dependent ones. Typically each DataFrame is univariate in respect to a corresponding indenpendent variable.
        :rtype pandas.DataFrame:
        """

        keys_from_dependent_objs_ = list(self.dependent_objs.keys())

        kys_from_independent_vars = list(self.independent_vars.keys())

        objs_names_ = kys_from_independent_vars+keys_from_dependent_objs_

        data_frame_ = pandas.DataFrame(index=objs_names_)

        return data_frame_
