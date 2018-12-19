# *coding:utf-8*

"""
Define Domain class, which distributes one equation among a domain of variables.  
"""

import pandas as pd
from .error_definitions import UnexpectedValueError
import numpy as np
from collections import OrderedDict
from itertools import product

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

        # print("\n->independent_vars:%s"%self.independent_vars)

        self.dependent_objs = OrderedDict({})

        self.description = description

        self.lower_bound = lower_bound

        self.upper_bound = upper_bound

        self.values = None

        self.is_set = False

    def __call__(self, independent_vars=None):

        """
        """

        self._setDomain(independent_vars)

    def __getitem__(self, idx):

        """
        """

        ind_vars = idx[0]

        dep_headers = idx[1]

        if not isinstance(ind_vars, list):

            ind_vars = [ind_vars]

        if not isinstance(dep_headers, list):

            dep_headers = [dep_headers]

        return np.array([self.values[i][j].values for (i,j) in product(ind_vars,dep_headers)])





    def _setDomain(self, independent_vars=None):

        """
        Set the independent variables on which the current domain rely on. Currently only unidimensional domains are suported.

        :ivar list(Variable) independent_vars:
            Independent vars on which the current domain rely on. Currently only unidimensional domains are suported.
        """

        if independent_vars == None:

            independent_vars = list(self.independent_vars.values())

        try:

            self.values = {var_i.name: self._createDataFramePrototype() for var_i in independent_vars}

        except:

            raise UnexpectedValueError("list(Variables)")

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

        if not isinstance(values, np.ndarray):

            values = np.array(values)

        # print("\nShape of values is {}".format(values.shape))

        if var==None:

            var = list(self.independent_vars.values())[-1]

        if self.values[var.name].values.size ==0 :

            self.values[var.name] =  pd.DataFrame(values,columns=self.values[var.name].columns)
        elif self.values[var.name].values.size > 0 and values.shape[1] == len(self.independent_vars.keys())+len(self.dependent_objs.keys()):

            self.values[var.name] =  pd.DataFrame(np.vstack((self.values[var.name].values, values)),columns=self.values[var.name].index)

        else:

            raise Exception("Error. Ill-formed input for domain register")

    def _createDataFramePrototype(self):

        """
        Create the prototype of DataFrame for the independent variables and dependent ones

        :return data_frame_:
            Prototype of DataFrame including all the independent variables and the dependent ones. Typically each DataFrame is univariate in respect to a corresponding indenpendent variable.
        :rtype pandas.DataFrame:
        """

        # print("\n~>dependent_objs: %s"%self.dependent_objs)

        keys_from_dependent_objs = list(self.dependent_objs.keys())

        keys_from_independent_vars = list(self.independent_vars.keys())

        objs_names = keys_from_independent_vars+keys_from_dependent_objs

        # print("\n~>Creating prototype with indexes: %s"%objs_names)

        data_frame_ = pd.DataFrame(columns=objs_names)

        return data_frame_

    def _renameHeaders(self, variable_name_map):

        """
        Rename the column headers of the domain using the mapping provided

        :param dict variable_name_map:
            Dictionary containing the original name of the variables in the domain, and the corresponding name which will be modified.
        """

        for i,key in enumerate(list(self.values.keys())):

            self.values[key].rename(columns=variable_name_map, inplace=True)
