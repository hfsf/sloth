#test_parameter.py

from pathlib import Path
import sys

root_dir = Path(Path.cwd()).parent

sys.path.append(str(root_dir))#+'/src/')

import pytest

from src.sloth.core import parameter
from src.sloth.core import template_units

import copy

@pytest.fixture
def param():
    """
    Create a generic Parameter object with generic name, description and no value defined
    """

    return parameter.Parameter("generic_param",template_units.kg_s,"A generic param")

def test_param_properties(param):

    assert param.name == "generic_param"
    assert dict(param.units.dimension) == pytest.approx({'m':0.0,'kg':1.,'s':-1,'A':0.0,'K':0.0,'mol':0.0,'cd':0.0})
    assert param.description == "A generic param"

def test_set_param_value(param):

    param.setValue(10)

    assert param.value == 10


@pytest.mark.parametrize("name,latex_text,operation", [
    ("a","a","+"),
    ("b","b","-"),
    ("c","c","*"),
    ("d","d","/"),
    ("e","e","^")
])

def test_operations(param, name, latex_text, operation):
    param.name = name
    param.latex_text = latex_text

    other = copy.deepcopy(param)
    other.name = 'other_'+param.name
    other.latex_text = other.name

    #print("\n->param:{} param type:{}\nother:{} other type:{}".format(param,type(param),other,type(other)))
    #print("\nparam dict:{}\n\nother dict:{}".format(param.__dict__, other.__dict__))

    # Create an EquationNode

    if operation == "+":

        result = param() + other()

        result_name = param.name+operation+other.name

        latex_result = param.name+"+"+other.name

        op_unit_result = str(param.units+other.units)

    elif operation == "-":

        result = param() - other()

        result_name = param.name+operation+other.name

        latex_result = param.name+"-"+other.name

        op_unit_result = str(param.units-other.units)

    elif operation == "*":

        result = param() * other()

        result_name = param.name+operation+other.name

        latex_result = param.name+"*"+other.name

        op_unit_result = str(param.units*other.units)

    elif operation == "/":

        result = param() / other()

        result_name = param.name+operation+other.name

        latex_result = "\\frac{"+param.name+"}{"+other.name+"}"

        op_unit_result = str(param.units/other.units)

    elif operation == "^":

        result = param() ** 2

        result_name = param.name+"**2"

        latex_result = param.name+"^2"

        op_unit_result = str(param.units**2)        

    #print("\n result dict:{}".format(result.__dict__))

    assert result.name == result_name and \
           str(result.unit_object) == op_unit_result and \
           result.latex_text == latex_result
