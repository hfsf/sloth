# *coding:utf-8*

"""
Define EquationNode class, that holds the reference to variables in the equations
"""

from .error_definitions import UnexpectedValueError, DimensionalCoherenceError

class EquationNode:

    """
    Definition of an EquationNode (ENODE). Represent an object from which arithmetical operations can be performed.

    * TODO:
        - Include comparison operators for EquationNode objects (<,>,<=,>=,etc) as unary operation that compares values directly.
        - Include overloading of power operators for EquationNode objects
        - Include Conditional evaluation operator (IfThen) as binary operations
          Eg: IfThen(CONDITION, [THEN_CLAUSE,ELSE_CAUSE]) 
    """

    def __init__(self, name='', symbolic_object=None, symbolic_map=[], unit_object=None, args=[], latex_text=''):

        """
        Instantiate EquationNode

        :ivar str name:
            Name for the current ENODE. Defaults to "".

        :ivar sympy.symbols symbolic_object:
            Base symbolic object for which arithmetical operations are evaluated. Defaults to None.

        :ivar list symbolic_map:
            Dictionary containing the mapping beetween the symbolic objects and their corresponding Quantity objects for ENODE re-evaluation.

        :ivar Unit unit_object:
            Unit object corresponding to the dimension of ENODE.

        :ivar list args:
            List of additional arguments for ENODE. Currently, included for future use. Defaults to [].

        :ivar str latex_text:
            Latex text representing the current ENODE. Defaults to "".
        """
        
        self.name = name

        self.symbolic_object = symbolic_object

        self.symbolic_map = symbolic_map

        self.unit_object = unit_object

        self.args = args

        self.latex_text = latex_text

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
                                name="+".join([self.name, other_obj.name]), \
                                symbolic_object=self.symbolic_object+other_obj.symbolic_object, \
                                symbolic_map={**self.symbolic_map, **other_obj.symbolic_map}, \
                                unit_object=self.unit_object+other_obj.unit_object,
                                latex_text=self.latex_text+"+"+other_obj.latex_text
                                )

            return(enode_)

        elif isinstance(other_obj, int) or isinstance(other_obj, float):

            enode_ = self.__class__(
                            name="+".join([self.name, str(other_obj)]), \
                            symbolic_object=self.symbolic_object+other_obj,
                            symbolic_map={**self.symbolic_map}, \
                            unit_object=self.unit_object, \
                            latex_text=self.latex_text+"+"+str(other_obj)
                                )

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
                                name="-".join([self.name, other_obj.name]), \
                                symbolic_object=self.symbolic_object-other_obj.symbolic_object, \
                                symbolic_map={**self.symbolic_map, **other_obj.symbolic_map}, \
                                unit_object=self.unit_object-other_obj.unit_object,
                                latex_text=self.latex_text+"-"+other_obj.latex_text
                                )

            return(enode_)

        elif isinstance(other_obj, int) or isinstance(other_obj, float):

            enode_ = self.__class__(
                            name="-".join([self.name, str(other_obj)]), \
                            symbolic_object=self.symbolic_object-other_obj,
                            symbolic_map={**self.symbolic_map}, \
                            unit_object=self.unit_object, \
                            latex_text=self.latex_text+"-"+str(other_obj)
                                )

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
                                name="*".join([self.name, other_obj.name]), \
                                symbolic_object=self.symbolic_object*other_obj.symbolic_object, \
                                symbolic_map={**self.symbolic_map, **other_obj.symbolic_map}, \
                                unit_object=self.unit_object*other_obj.unit_object,
                                latex_text=self.latex_text+"*"+other_obj.latex_text
                                )

            return(enode_)

        elif isinstance(other_obj, int) or isinstance(other_obj, float):

            enode_ = self.__class__(
                            name="*".join([self.name, str(other_obj)]), \
                            symbolic_object=self.symbolic_object*other_obj,
                            symbolic_map={**self.symbolic_map}, \
                            unit_object=self.unit_object, \
                            latex_text=self.latex_text+"*"+str(other_obj)
                                )

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
                                name="/".join([self.name, other_obj.name]), \
                                symbolic_object=self.symbolic_object/other_obj.symbolic_object, \
                                symbolic_map={**self.symbolic_map, **other_obj.symbolic_map}, \
                                unit_object=self.unit_object/other_obj.unit_object,
                                latex_text="\\frac{"+self.latex_text+"}{"+other_obj.latex_text+"}"
                                )

            return(enode_)

        elif isinstance(other_obj, int) or isinstance(other_obj, float):

            enode_ = self.__class__(
                        name="/".join([self.name, str(other_obj)]), \
                        symbolic_object=self.symbolic_object/other_obj,
                        symbolic_map={**self.symbolic_map}, \
                        unit_object=self.unit_object, \
                        latex_text="\\frac{"+self.latex_text+"}{"+str(other_obj)+"}"
                                )

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
                                name="/".join([self.name, other_obj.name]), \
                                symbolic_object=self.symbolic_object/other_obj.symbolic_object, \
                                symbolic_map={**self.symbolic_map, 
                                                **other_obj.symbolic_map}, \
                                unit_object=self.unit_object/other_obj.unit_object,
                                latex_text="\\frac{"+self.latex_text+"}{"+other_obj.latex_text+"}"
                                )

            return(enode_)

        elif isinstance(other_obj, int) or isinstance(other_obj, float):

            enode_ = self.__class__(
                        name="/".join([self.name, str(other_obj)]), \
                        symbolic_object=self.symbolic_object/other_obj,
                        symbolic_map={**self.symbolic_map}, \
                        unit_object=self.unit_object, \
                        latex_text="\\frac{"+self.latex_text+"}{"+str(other_obj)+"}"
                                )

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
                                    name="**".join([self.name, other_obj.name]), \
                                    symbolic_object=self.symbolic_object**other_obj.symbolic_object, \
                                    symbolic_map={**self.symbolic_map, 
                                                    **other_obj.symbolic_map
                                                  }, \
                                    unit_object=self.unit_object**other_obj.unit_object,
                                    latex_text=self.latex_text+"^"+other_obj.latex_text
                                    )

                return(enode_)

            else:

                raise DimensionalCoherenceError(other_obj.unit_object, None)
        
        elif isinstance(other_obj, int) or isinstance(other_obj, float):

                enode_ = self.__class__(
                                name="**".join([self.name, str(other_obj)]), \
                                symbolic_object=self.symbolic_object**other_obj,
                                symbolic_map={**self.symbolic_map}, \
                                unit_object=self.unit_object**other_obj, \
                                latex_text=self.latex_text+"^"+str(other_obj)
                                    )

                return(enode_)

        else:

            raise UnexpectedValueError("(int, float, EquationNode)")