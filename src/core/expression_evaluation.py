# *coding:utf-8*

"""
Define EquationNode class, that holds the reference to variables in the equations
"""

from .error_definitions import UnexpectedValueError, DimensionalCoherenceError
import sympy as sp

class EquationNode:

    """
    Definition of an EquationNode (ENODE). Represent an object from which arithmetical operations can be performed.

    * TODO:
        - Include comparison operators for EquationNode objects (<,>,<=,>=,etc) as unary operation that compares values directly.
        - Include Conditional evaluation operator (IfThen) as binary operations
          Eg: IfThen(CONDITION, [THEN_CLAUSE,ELSE_CAUSE]) 
    """

    def __init__(self, name='', symbolic_object=None, symbolic_map={}, variable_map={}, is_linear=True, is_nonlinear=False, is_differential=False, unit_object=None, args=[], latex_text='', repr_symbolic=None):

        """
        Instantiate EquationNode

        :ivar str name:
            Name for the current ENODE. Defaults to "".

        :ivar sympy.symbols symbolic_object:
            Base symbolic object for which arithmetical operations are evaluated. Defaults to None.

        :ivar dict symbolic_map:
            Dictionary containing the mapping beetween the symbolic objects and their corresponding Quantity objects

        :ivar dict variable_map:
            Dictionary containing only the mapping beetween the synmbolic objects and their corresponding Quantity objects that were not specified (eg:Variable, unespecified Parameter, etc)

        : ivar bool is_linear:
            If the current ENODE contains a linear expression

        : ivar bool is_nonlinear:
            If the current ENODE contains a nonlinear expression

        : ivar bool is_differential:
            If the current ENODE contains a differential expression

        :ivar Unit unit_object:
            Unit object corresponding to the dimension of ENODE.

        :ivar list args:
            List of additional arguments for ENODE. Currently, included for future use. Defaults to [].

        :ivar str latex_text:
            Latex text representing the current ENODE. Defaults to "".

        :ivar str repr_symbolic:
            Symbolic representation of the symbolic object for which arithmetical operations are evaluated, used for ENODE conversion to string. Defaults to None.
        """
        
        self.name = name

        self.symbolic_object = symbolic_object

        self.symbolic_map = symbolic_map

        self.variable_map = variable_map

        self.equation_type = {'is_linear':is_linear, \
                              'is_nonlinear':is_nonlinear, \
                              'is_differential':is_differential
                             }

        self.unit_object = unit_object

        self.args = args

        self.latex_text = latex_text

        self.repr_symbolic = repr_symbolic

    def _checkEquationTypePrecedence(self, eq_type_1, eq_type_2):

        res = {'is_linear':False, 'is_nonlinear':False, 'is_differential':False}

        if eq_type_1['is_differential'] == True or \
           eq_type_2['is_differential'] == True:

            res['is_differential'] = True

            return res
        
        elif eq_type_1['is_nonlinear'] == True or \
             eq_type_2['is_nonlinear'] == True:

            res['is_nonlinear'] = True

            return res

        else:

            res['is_linear'] = True

            return res

    def __str__(self):

        """
        Overloaded representation of the ENODE object. Returns a symbolic representation of the equation decribed by the object.

        :return:
            Return a string representing the symbolic object that represents the equation described by the current ENODE
        :rtype str:
        """

        return str(self.symbolic_object)

    def __repr__(self):

        """
        Overloaded representation of the ENODE object. Returns a fully symbolic representation of the equation decribed by the object.

        :return:
            Return a string representing the symbolic object that represents the equation described by the current ENODE (fully symbolic)
        :rtype str:
        """

        return str(self.repr_symbolic)

    def __eq__(self, other_obj):

        """
        Overloaded function for definition of the relation beetween ENODE objects. Tipically used for construction of equation expressions in the elementary form (a + b == c) instead of the residual form (a + b -c )

        :param ENODE other_obj:
            Second ENODE object for which mathematical operation will be performed.

        :return:
            Return a new tuple of ENODE corresponding to the result of mathematical operation in the elementary form.
        :rtype tuple(EquationNode, EquationNode):
        """

        if isinstance(other_obj, self.__class__):

            return tuple([self, other_obj])

        else:

            return UnexpectedValueError("EquationNode")

    def __add__(self, other_obj):

        """
        Overloaded function for summation of ENODE object. The __add__ function calls self.unit_object._check_dimensional_coherence.

        :param ENODE other_obj:
            Second ENODE object for which mathematical operation will be performed.

        :return:
            Return a new ENODE corresponding to the result of mathematical operation.
        :rtype EquationNode:
        """

        # * === Code snippet only work on Python 3.5+ ===

        if isinstance(other_obj, self.__class__):

            # other_obj is another ENODE.

            enode_ = self.__class__(
                                name="+".join([self.name, other_obj.name]),
                                symbolic_object=self.symbolic_object+other_obj.symbolic_object,
                                symbolic_map={**self.symbolic_map, **other_obj.symbolic_map},
                                variable_map={**self.variable_map, **other_obj.variable_map},
                                unit_object=self.unit_object+other_obj.unit_object,
                                latex_text="+".join([self.latex_text,other_obj.latex_text]),
                                repr_symbolic=self.repr_symbolic+other_obj.repr_symbolic
                                )

            enode_.equation_type = self._checkEquationTypePrecedence(self.equation_type, other_obj.equation_type)

            return(enode_)

        elif isinstance(other_obj, int) or isinstance(other_obj, float):

            # other_obj is a numerical value

            enode_ = self.__class__(
                            name="+".join([self.name, str(other_obj)]), 
                            symbolic_object=self.symbolic_object+other_obj,
                            symbolic_map={**self.symbolic_map}, 
                            variable_map={**self.variable_map},
                            unit_object=self.unit_object, 
                            latex_text=self.latex_text+"+"+str(other_obj),
                            repr_symbolic=self.repr_symbolic+other_obj
                                )

            enode_.equation_type = {**self.equation_type}

            return(enode_)

        else:

            raise UnexpectedValueError("(int, float, EquationNode)")

    def __sub__(self, other_obj):

        """
        Overloaded function for subtraction of ENODE object. The __sub__ function calls self.unit_object._check_dimensional_coherence.

        :param ENODE other_obj:
            Second ENODE object for which mathematical operation will be performed.

        :return:
            Return a new ENODE corresponding to the result of mathematical operation.
        :rtype EquationNode:
        """

        # * === Code snippet only work on Python 3.5+ ===


        if isinstance(other_obj, self.__class__):

            # other_obj is another ENODE.

            enode_ = self.__class__(
                                name="-".join([self.name, other_obj.name]), 
                                symbolic_object=self.symbolic_object-other_obj.symbolic_object, 
                                symbolic_map={**self.symbolic_map, **other_obj.symbolic_map},
                                variable_map={**self.variable_map, **other_obj.variable_map}, 
                                unit_object=self.unit_object-other_obj.unit_object,
                                latex_text="-".join([self.latex_text,other_obj.latex_text]),                  
                                repr_symbolic=self.repr_symbolic-other_obj.repr_symbolic
                                )

            enode_.equation_type = self._checkEquationTypePrecedence(self.equation_type, other_obj.equation_type)

            return(enode_)

        elif isinstance(other_obj, int) or isinstance(other_obj, float):

            enode_ = self.__class__(
                            name="-".join([self.name, str(other_obj)]), 
                            symbolic_object=self.symbolic_object-other_obj,
                            symbolic_map={**self.symbolic_map},
                            variable_map={**self.variable_map}, 
                            unit_object=self.unit_object, 
                            latex_text=self.latex_text+"-"+str(other_obj),
                            repr_symbolic=self.repr_symbolic-other_obj
                                )

            enode_.equation_type = {**self.equation_type}

            return(enode_)

        else:

            raise UnexpectedValueError("(int, float, EquationNode)")

    def __mul__(self, other_obj):

        """
        Overloaded function for multiplication of ENODE object. The __mul__ function process the resultant dimension accordingly.

        :param ENODE other_obj:
            Second ENODE object for which mathematical operation will be performed.

        :return:
            Return a new ENODE corresponding to the result of mathematical operation.
        :rtype EquationNode:
        """

        # * === Code snippet only work on Python 3.5+ ===

        if isinstance(other_obj, self.__class__):

            # other_obj is another ENODE.

            enode_ = self.__class__(
                                name="*".join([self.name, other_obj.name]), 
                                symbolic_object=self.symbolic_object*other_obj.symbolic_object, 
                                symbolic_map={**self.symbolic_map, **other_obj.symbolic_map},
                                variable_map={**self.variable_map, **other_obj.variable_map}, 
                                unit_object=self.unit_object*other_obj.unit_object,
                                latex_text="*".join([self.latex_text,other_obj.latex_text]),                  
                                repr_symbolic=self.repr_symbolic*other_obj.repr_symbolic                                
                                )

            enode_.equation_type = self._checkEquationTypePrecedence(self.equation_type, other_obj.equation_type)

            return(enode_)

        elif isinstance(other_obj, int) or isinstance(other_obj, float):

            enode_ = self.__class__(
                            name="*".join([self.name, str(other_obj)]), 
                            symbolic_object=self.symbolic_object*other_obj,
                            symbolic_map={**self.symbolic_map},
                            variable_map={**self.variable_map}, 
                            unit_object=self.unit_object, 
                            latex_text=self.latex_text+"*"+str(other_obj),
                            repr_symbolic=self.repr_symbolic*other_obj
                                )

            enode_.equation_type = {**self.equation_type}

            return(enode_)

        else:

            raise UnexpectedValueError("(int, float, EquationNode)")


    def __div__(self, other_obj):

        """
        Overloaded function for division of ENODE object. The __div__ function process the resultant dimension accordingly.

        :param ENODE other_obj:
            Second ENODE object for which mathematical operation will be performed.

        :return:
            Return a new ENODE corresponding to the result of mathematical operation.
        :rtype EquationNode:
        """

        # * === Code snippet only work on Python 3.5+ ===

        if isinstance(other_obj, self.__class__):

            # other_obj is another ENODE.

            enode_ = self.__class__(
                                name="/".join([self.name, other_obj.name]), 
                                symbolic_object=self.symbolic_object/other_obj.symbolic_object, 
                                symbolic_map={**self.symbolic_map, **other_obj.symbolic_map},
                                variable_map={**self.variable_map, **other_obj.variable_map}, 
                                unit_object=self.unit_object/other_obj.unit_object,
                                latex_text="\\frac{"+self.latex_text+"}{"+other_obj.latex_text+"}",             
                                repr_symbolic=self.repr_symbolic/other_obj.repr_symbolic       
                                )

            enode_.equation_type = self._checkEquationTypePrecedence(self.equation_type, other_obj.equation_type)

            return(enode_)

        elif isinstance(other_obj, int) or isinstance(other_obj, float):

            enode_ = self.__class__(
                        name="/".join([self.name, str(other_obj)]),
                        symbolic_object=self.symbolic_object/other_obj,
                        symbolic_map={**self.symbolic_map},
                        variable_map={**self.variable_map},
                        unit_object=self.unit_object,
                        latex_text="\\frac{"+self.latex_text+"}{"+str(other_obj)+"}",
                        repr_symbolic=self.repr_symbolic/other_obj
                        )

            enode_.equation_type = {**self.equation_type}

            return(enode_)

        else:

            raise UnexpectedValueError("(int, float, EquationNode)")


    def __truediv__(self, other_obj):

        """
        Overloaded function for true division of ENODE object. The __truediv__ function process the resultant dimension accordingly. 

        :param ENODE other_obj:
            Second ENODE object for which mathematical operation will be performed.

        :return:
            Return a new ENODE corresponding to the result of mathematical operation.
        :rtype EquationNode:
        """

        # * === Code snippet only work on Python 3.5+ ===

        if isinstance(other_obj, self.__class__):

            # other_obj is another ENODE.

            enode_ = self.__class__(
                                name="/".join([self.name, other_obj.name]),
                                symbolic_object=self.symbolic_object/other_obj.symbolic_object,
                                symbolic_map={**self.symbolic_map, **other_obj.symbolic_map},
                                variable_map={**self.variable_map, **other_obj.variable_map},
                                unit_object=self.unit_object/other_obj.unit_object,
                                latex_text="\\frac{"+self.latex_text+"}{"+other_obj.latex_text+"}",             
                                repr_symbolic=self.repr_symbolic/other_obj.repr_symbolic   
                                )

            enode_.equation_type = self._checkEquationTypePrecedence(self.equation_type, other_obj.equation_type)

            return(enode_)

        elif isinstance(other_obj, int) or isinstance(other_obj, float):

            enode_ = self.__class__(
                        name="/".join([self.name, str(other_obj)]),
                        symbolic_object=self.symbolic_object/other_obj,
                        symbolic_map={**self.symbolic_map},
                        variable_map={**self.variable_map},
                        unit_object=self.unit_object,
                        latex_text="\\frac{"+self.latex_text+"}{"+str(other_obj)+"}",
                        repr_symbolic=self.repr_symbolic/other_obj
                                )

            enode_.equation_type = {**self.equation_type}

            return(enode_)

        else:

            raise UnexpectedValueError("(int, float, EquationNode)")


    def __pow__(self, other_obj):

        """
        Overloaded function for power of ENODE object. The __pow__ function check the dimensional coherence through other_obj.unit_object._is_dimensionless

        :param ENODE other_obj:
            Second ENODE object for which mathematical operation will be performed.

        :return:
            Return a new ENODE corresponding to the result of mathematical operation.
        :rtype EquationNode:
        """

        # * === Code snippet only work on Python 3.5+ ===

        if isinstance(other_obj, self.__class__):

            # other_obj is another ENODE.

            if other_obj.unit_object._is_dimensionless() == True:

                #other_obj is dimensionless

                enode_ = self.__class__(
                                    name="**".join([self.name, other_obj.name]),
                                    symbolic_object=self.symbolic_object**other_obj.symbolic_object,
                                    symbolic_map={**self.symbolic_map, **other_obj.symbolic_map},
                                    variable_map={**self.variable_map, **other_obj.variable_map},
                                    unit_object=self.unit_object**other_obj.unit_object,
                                    latex_text=self.latex_text+"^"+other_obj.latex_text,             
                                    repr_symbolic=self.repr_symbolic**other_obj.repr_symbolic   
                                    )

                enode_.equation_type = self._checkEquationTypePrecedence(self.equation_type, {'is_linear':False, 'is_nonlinear':True, 'is_differential':False})

                return(enode_)

            else:

                raise DimensionalCoherenceError(other_obj.unit_object, None)
        
        elif isinstance(other_obj, int) or isinstance(other_obj, float):

            enode_ = self.__class__(
                            name="**".join([self.name, str(other_obj)]),
                            symbolic_object=self.symbolic_object**other_obj,
                            symbolic_map={**self.symbolic_map},
                            variable_map={**self.variable_map},
                            unit_object=self.unit_object**other_obj,
                            latex_text=self.latex_text+"^"+str(other_obj),
                            repr_symbolic=self.repr_symbolic**other_obj
                            )

            enode_.equation_type = self._checkEquationTypePrecedence(self.equation_type, {'is_linear':False, 'is_nonlinear':True, 'is_differential':False})

            return(enode_)

        else:

            raise UnexpectedValueError("(int, float, EquationNode)")