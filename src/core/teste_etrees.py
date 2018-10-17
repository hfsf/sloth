import Variable
import Equation
import template_units as tu

a = Variable.Variable("a",tu.kg,value=10.)
b = Variable.Variable("b",tu.kg,value=11.)
c = Variable.Variable("c",tu.kg,value=12.)
d = Variable.Variable("d",tu.kg,value=13.)
e = Variable.Variable("e",tu.kg,value=14.)
f = Variable.Variable("f",tu.kg,value=15.)


eq = Equation.Equation("a+b+c","generic test equation for a+b+c")

eq.setResidual(a()+b()+c()+d()+e()+f())

eq.evalResidual()
