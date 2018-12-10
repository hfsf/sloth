#test_variable.py

"""
from pathlib import Path
import sys

root_dir = Path(Path.cwd()).parent

sys.path[0] = str(root_dir)+'/src/'
"""

import pytest

from .core import variable
from .core import template_units

import copy

@pytest.fixture
def var():
    """
    Create a generic Variable object with generic name, description and no value defined
    """

    return variable.Variable("generic_var",template_units.kg_s,"A generic var")

def test_var_properties(var):

    assert var.name == "generic_var" and \
           str(var.units) == "kg^1 s^-1" and \
           var.description == "A generic var"

def test_set_var_value(var):

    var.setValue(10)

    assert var.value == 10


@pytest.mark.parametrize("name,latex_text,operation", [
    ("a","a","+"),
    ("b","b","-"),
    ("c","c","*"),
    ("d","d","/"),
    ("e","e","^")
])

def test_operations(var, name, latex_text, operation):
    var.name = name
    var.latex_text = latex_text

    other = copy.deepcopy(var)
    other.name = 'other_'+var.name
    other.latex_text = other.name

    #print("\n->var:{} var type:{}\nother:{} other type:{}".format(var,type(var),other,type(other)))
    #print("\nvar dict:{}\n\nother dict:{}".format(var.__dict__, other.__dict__))

    # Create an EquationNode

    if operation == "+":

        result = var() + other()

        result_name = var.name+operation+other.name

        latex_result = var.name+"+"+other.name

        op_unit_result = str(var.units+other.units)

    elif operation == "-":

        result = var() - other()

        result_name = var.name+operation+other.name

        latex_result = var.name+"-"+other.name

        op_unit_result = str(var.units-other.units)

    elif operation == "*":

        result = var() * other()

        result_name = var.name+operation+other.name

        latex_result = var.name+"*"+other.name

        op_unit_result = str(var.units*other.units)

    elif operation == "/":

        result = var() / other()

        result_name = var.name+operation+other.name

        latex_result = "\\frac{"+var.name+"}{"+other.name+"}"

        op_unit_result = str(var.units/other.units)

    elif operation == "^":

        result = var() ** 2

        result_name = var.name+"**2"

        latex_result = var.name+"^2"

        op_unit_result = str(var.units**2)        

    #print("\n result dict:{}".format(result.__dict__))

    assert result.name == result_name and \
           str(result.unit_object) == op_unit_result and \
           result.latex_text == latex_result


def test_operation_with_numeric_and_enodes(var):

    assert var() + 2. == 2. + var() and \
           1. - var() == var()*-1 + 1. and \
           var()**-1 == 1./var() and \
           2*var() == var() + var()



