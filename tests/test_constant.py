# test_constant.py

from pathlib import Path
import sys

root_dir = Path(Path.cwd()).parent

sys.path.append(str(root_dir))#+'/src/')

import pytest

from src.sloth.core import constant
from src.sloth.core import template_units

import copy


@pytest.fixture
def const():
    """
    Create a generic Constant object with generic name, description and no value defined
    """

    return constant.Constant("generic_const",template_units.kg_s,"A generic const")

def test_const_properties(const):

    assert const.name == "generic_const"
    assert str(const.units.dimension) == pytest.approx({'m':0.0,'kg':1.,'s':-1,'A':0.0,'K':0.0,'mol':0.0,'cd':0.0})
    assert const.description == "A generic const"

def test_set_const_value(const):

    const.setValue(10)

    assert const.value == 10


@pytest.mark.parametrize("name,latex_text,operation", [
    ("a","a","+"),
    ("b","b","-"),
    ("c","c","*"),
    ("d","d","/"),
    ("e","e","^")
])

def test_operations(const, name, latex_text, operation):
    const.name = name
    const.latex_text = latex_text

    other = copy.deepcopy(const)
    other.name = 'other_'+const.name
    other.latex_text = other.name

    #print("\n->const:{} const type:{}\nother:{} other type:{}".format(const,type(const),other,type(other)))
    #print("\nconst dict:{}\n\nother dict:{}".format(const.__dict__, other.__dict__))

    # Create an EquationNode

    if operation == "+":

        result = const() + other()

        result_name = const.name+operation+other.name

        latex_result = const.name+"+"+other.name

        op_unit_result = str(const.units+other.units)

    elif operation == "-":

        result = const() - other()

        result_name = const.name+operation+other.name

        latex_result = const.name+"-"+other.name

        op_unit_result = str(const.units-other.units)

    elif operation == "*":

        result = const() * other()

        result_name = const.name+operation+other.name

        latex_result = const.name+"*"+other.name

        op_unit_result = str(const.units*other.units)

    elif operation == "/":

        result = const() / other()

        result_name = const.name+operation+other.name

        latex_result = "\\frac{"+const.name+"}{"+other.name+"}"

        op_unit_result = str(const.units/other.units)

    elif operation == "^":

        result = const() ** 2

        result_name = const.name+"**2"

        latex_result = const.name+"^2"

        op_unit_result = str(const.units**2)        

    #print("\n result dict:{}".format(result.__dict__))

    assert result.name == result_name and \
           str(result.unit_object) == op_unit_result and \
           result.latex_text == latex_result
