"""
Define functions for utilization in the equation writing.
All those functions return EquationNode objects.
"""
import sympy as sp
import numpy as np
from .expression_evaluation import EquationNode
from .template_units import dimless
# import error_definitions as errors


"""
Transcedental functions for utilization in the equation definition
"""

def _Log10(sp_obj, evaluate=True):

    return(sp.log(sp_obj,10,evaluate=evaluate))

def wrapper(own_func, obj, base_func, latex_func_name=None, equation_type=None, dim_check=True, ind_var=None):

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
                                  variable_map={},
                                  unit_object=dimless,
                                  latex_text=f_name(latex_func_name, str(obj)),
                                  repr_symbolic=base_func(obj, evaluate=False)
                                )

            return enode_

        elif isinstance(obj, EquationNode) == True:

            if obj.unit_object._is_dimensionless() == True or dim_check == False:

                # obj is an EquationNode

                enode_ = EquationNode(name=f_name(own_func.__name__, obj.name),
                                symbolic_object=base_func(obj.symbolic_object, evaluate=False),
                                symbolic_map={**obj.symbolic_map},
                                variable_map={**obj.variable_map},
                                unit_object=obj.unit_object,
                                latex_text=f_name(latex_func_name, obj.latex_text),
                                repr_symbolic=base_func(obj.repr_symbolic, evaluate=False)
                                )

                enode_.equation_type = equation_type_

                return enode_

            else:

                raise TypeError("A dimensionless argument was expected \n %s" % obj.unit_object.dimension)

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

def Min(*obj):

    obj = list(obj)

    latex_func_name = "min"

    f_name = latex_func_name+"\\right ("

    obj_symb_map = {}

    obj_var_map = {}

    obj_symb_objcts = []

    for obj_i in obj:

        if hasattr(obj_i,'obj_latex_name'):

            obj_latex_name = obj_i.obj_latex_name

        else:

            try:

                obj_latex_name = obj_i.name

            except:

                obj_latex_name = str(obj_i)

        if isinstance(obj_i, EquationNode):

            obj_name = obj_i.name

        else:

            obj_name = str(obj_i)

            obj_latex_name = str(obj_i)

        f_name+=obj_name

        if hasattr(obj_i, 'symbolic_object'):

            obj_symb_objcts.append(obj_i.symbolic_object)

        else:

            obj_symb_objcts.append(obj_i)

        #Gather all the symbolic and variable map from the obj

        try:

            obj_symb_map = {**obj_symb_map, **obj_i.symbolic_map}

            obj_var_map = {**obj_var_map, **obj_i.variable_map}

        except:

            pass

    f_name += ")"

    latex_func_name+="\\right )"

    if all(isinstance(obj_i, float) or isinstance(obj_i, int) for obj_i in obj):

        obj_dims = dimless

    elif all(isinstance(obj_i, EquationNode) for obj_i in obj):

        if all(the_unit == obj[0].unit_object for the_unit in obj):

            obj_dims = obj[0].unit_object

        else:

            raise UnexpectedValueError("A set of objects with equivalent dimensions")

    else:

        obj_dims = [obj_i.unit_object for obj_i in obj if hasattr(obj_i,'unit_object')][0]

        if obj_dims is []:

            obj_dims = dimless

    enode_ = EquationNode(name=f_name,
                          symbolic_object=sp.Min(*obj_symb_objcts, evaluate=False),
                          symbolic_map=obj_symb_map,
                          variable_map=obj_var_map,
                          unit_object=obj_dims,
                          latex_text=latex_func_name,
                          repr_symbolic=sp.Min(*obj_symb_objcts, evaluate=False)
                        )

    return enode_

def Max(*obj):

    obj = list(obj)

    latex_func_name = "max"

    f_name = latex_func_name+"\\right ("

    obj_symb_map = {}

    obj_var_map = {}

    obj_symb_objcts = []

    for obj_i in obj:

        if hasattr(obj_i,'obj_latex_name'):

            obj_latex_name = obj_i.obj_latex_name

        else:

            obj_latex_name = obj_i.name

        if isinstance(obj_i, EquationNode):

            obj_name = obj_i.name

        else:

            obj_name = str(obj_i)

            obj_latex_name = str(obj_i)

        f_name+=obj_name

        if hasattr(obj_i, 'symbolic_object'):

            obj_symb_objcts.append(obj_i.symbolic_object)

        else:

            obj_symb_objcts.append(obj_i)

        #Gather all the symbolic and variable map from the obj

        try:

            obj_symb_map = {**obj_symb_map, **obj_i.symbolic_map}

            obj_var_map = {**obj_var_map, **obj_i.variable_map}

        except:

            pass

    f_name += ")"
    latex_func_name+="\\right )"

    if all(isinstance(obj_i, float) or isinstance(obj_i, int) for obj_i in obj):

        obj_dims = dimless

    elif all(isinstance(obj_i, EquationNode) for obj_i in obj):

        if all(the_unit == obj[0].unit_object for the_unit in obj):

            obj_dims = obj[0].unit_object

        else:

            raise UnexpectedValueError("A set of objects with equivalent dimensions")

    else:

        obj_dims = [obj_i.unit_object for obj_i in obj if hasattr(obj_i,'unit_object')][0]

        if obj_dims is []:

            obj_dims = dimless

    enode_ = EquationNode(name=f_name,
                          symbolic_object=sp.Max(*obj_symb_objcts, evaluate=False),
                          symbolic_map=obj_symb_map,
                          variable_map=obj_var_map,
                          unit_object=obj_dims,
                          latex_text=latex_func_name,
                          repr_symbolic=sp.Max(*obj_symb_objcts, evaluate=False)
                        )

    return enode_

def _Diff(obj, ind_var_):

    #return wrapper(Diff, obj, sp.diff, equation_type={'is_differential':True}, dim_check=False, ind_var=ind_var_)

    equation_type_ = {'is_linear':False, 'is_nonlinear':False, 'is_differential':True}

    obj_ = obj.__call__()

    if hasattr(obj, 'Diff') != True:

        # obj is not an Variable instance (Dt method is absent)

        enode_ = EquationNode(name="Diff("+str(obj_)+")",
                              symbolic_object=0,
                              symbolic_map={},
                              variable_map={},
                              unit_object=dimless,
                              latex_text="Diff("+str(obj_)+")",
                              repr_symbolic=sp.diff(obj_, evaluate=False)
                            )

        return enode_

    else:

        # To get the independent variable for which Diff was defined

        if ind_var_ == None:

            symbolic_object_ = sp.diff(obj_.symbolic_object,
                              evaluate=False)
            repr_symbolic_ = sp.diff(obj_.repr_symbolic, evaluate=False)

            unit_object_ = dimless

        else:


            symbolic_object_ = symbolic_object=sp.diff(obj_.symbolic_object, ind_var_.__call__().symbolic_object, evaluate=False)

            repr_symbolic_ = sp.diff(obj_.repr_symbolic, ind_var_.__call__().repr_symbolic, evaluate=False)

            unit_object_ = obj_.unit_object/ind_var_.__call__().unit_object


        enode_ = EquationNode(name="Diff("+str(obj_)+")",
                              symbolic_object=symbolic_object_,
                              symbolic_map={**obj_.symbolic_map},
                              variable_map={**obj_.variable_map},
                              unit_object=unit_object_,
                              latex_text="Diff("+str(obj_)+")",
                              repr_symbolic=repr_symbolic_
                            )

        enode_.equation_type = equation_type_

        return enode_
