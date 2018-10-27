"""
Define functions for utilization in the equation writing.
All those functions return EquationNode objects.
"""
import sympy as sp
import numpy as np
from expression_evaluation import EquationNode
import error_definitions as errors


"""
Transcedental functions for utilization in the equation definition
"""

def _Log10(sp_obj):

    return(sp.log(sp_obj,10))

def wrapper(own_func, obj, base_func, latex_func_name=None):

        if latex_func_name == None:

            latex_func_name = own_func.__name__

        def f_name(func_name, obj_name):

            return(func_name+"("+obj_name+")")

        if isinstance(obj, float) or isinstance(obj, int):

            # obj is a number

            enode_ = EquationNode(name=f_name(own_func.__name__, str(obj)), \
                                  symbolic_object=base_func(obj), \
                                  symbolic_map={}, \
                                  latex_text=f_name(latex_func_name, str(obj))
                                )

            return enode_

        elif isinstance(obj, EquationNode) == True:

            if obj.unit_object._is_dimensionless() == True:

                # obj is an EquationNode

                enode_ = EquationNode(name=f_name(own_func.__name__, obj.name), \
                                symbolic_object=base_func(obj.symbolic_object), \
                                symbolic_map={**obj.symbolic_map}, \
                                latex_text=f_name(latex_func_name, obj.latex_text)
                                    )

                return enode_

            else:

                raise errors.NonDimensionalArgumentError(obj.unit_object)

        else:

            raise errors.UnexpectedValueError("(int, float, EquationNode)")            
def Log(obj):

    return wrapper(Log, obj, sp.log)

def Log10(obj):

    return wrapper(Log10, obj, _Log10)

def Sqrt(obj):

    return wrapper(Sqrt, obj, sp.sqrt)

def Abs(obj):

    return wrapper(Abs, obj, sp.Abs)

def Exp(obj):

    return wrapper(Exp, obj, sp.exp)

def Sin(obj):

    return wrapper(Sin, obj, sp.sin)

def Cos(obj):

    return wrapper(Cos, obj, sp.cos)

def Tan(obj):

    return wrapper(Tan, obj, sp.tan)