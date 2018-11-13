"""
Define functions for utilization in the equation writing.
All those functions return EquationNode objects.
"""
import sympy as sp
import numpy as np
from .expression_evaluation import EquationNode
from .template_units import dimless
#import error_definitions as errors


"""
Transcedental functions for utilization in the equation definition
"""

def _Log10(sp_obj, evaluate=True):

    return(sp.log(sp_obj,10,evaluate=evaluate))

def wrapper(own_func, obj, base_func, latex_func_name=None, equation_type=None):

        if equation_type == None:

            equation_type_ = {'is_linear':False, 'is_nonlinear':True, 'is_differential':False}
        else:

            equation_type_ = {'is_linear':False, 'is_nonlinear':False, 'is_differential':False}

            equation_type_.update(equation_type)            

        if latex_func_name == None:

            latex_func_name = own_func.__name__

        def f_name(func_name, obj_name):

            return(func_name+"("+obj_name+")")

        if isinstance(obj, float) or isinstance(obj, int):

            # obj is a number

            enode_ = EquationNode(name=f_name(own_func.__name__, str(obj)), 
                                  symbolic_object=base_func(obj, evaluate=False), 
                                  symbolic_map={}, 
                                  unit_object=dimless, 
                                  latex_text=f_name(latex_func_name, str(obj)),
                                  repr_symbolic=base_func(obj, evaluate=False)
                                )

            return enode_

        elif isinstance(obj, EquationNode) == True:

            if obj.unit_object._is_dimensionless() == True:

                # obj is an EquationNode

                enode_ = EquationNode(name=f_name(own_func.__name__, obj.name), 
                                symbolic_object=base_func(obj.symbolic_object, evaluate=False), 
                                symbolic_map={**obj.symbolic_map}, 
                                unit_object=dimless, 
                                latex_text=f_name(latex_func_name, obj.latex_text),
                                repr_symbolic=base_func(obj.repr_symbolic, evaluate=False)
                                )

                enode_.equation_type = equation_type_

                return enode_

            else:

                raise errors.NonDimensionalArgumentError(obj.unit_object)

        else:

            # Defined directly to avoid circular dependency error while importing expression_evaluation

            raise TypeError("Unexpected value error. A (int, float, EquationNode) was expected, but one divergent type was supplied.")            
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

def Dt(obj):

    return wrapper(Dt, obj, sp.diff, equation_type={'is_differential':True})