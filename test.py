import dbprobs
from outputroutines import output2latex, output2pdf
from problem import Problem, Assignment
d = dbprobs.__dict__

# generic test on all problems 
assignments = []
problems = []
for varname in d:
    if type(d[varname]) is Assignment:
        assignments.append(d[varname])
    elif type(d[varname]) is Problem:
        problems.append(d[varname])

def test_all_assignments(): # this is only the assignment class, not the problems subclassed in it
    for ass in assignments:
        ass.rng(len(ass)) # can be a number less than the number of problems

def test_all_problems():
    for prob in problems:
        for var in prob:
            var.rng()
        prob.solve()

def test_all_output2latex():
    for ass in assignments:
        output2latex(ass, 1)

def test_all_output2pdf():
    for ass in assignments:
        output2pdf(ass, 1)

from problem import *

def test_RandomUnit():
    print('random unit from dimensionality of SI unit of energy')
    ru = RandomUnit.from_unit_dimensionality('kg*m^2*s^-2')
    print('random unit "value"')
    print(ru.value)
    print('random unit unit set consistent with dimensionality')
    print(ru.unit_set)
    ru.rng()
    print('random unit "value" after rng')
    print(ru.value)
    print('random unit conversion factor from previous to current value')
    print(ru.conversion_factor)

def test_RandomQuantity():
    print('random quantity test')
    print('mass over length then squared')
    rsize = RandomSize( ((3,4),) )
    runit = RandomUnit(['kg/m','lb/ft','g/cm'])
    rq = RandomQuantity('rq',2,5,rsize,runit,3)
    res = rq.value*rq.value
    print(res)

def test_ConstantFloat():
    print('constant float test')
    rq2 = ConstantFloat('a', 2350)
    print(rq2.value)

if __name__ == '__main__':
    #test_all_assignments()
    #test_all_problems()
    #test_all_output2latex()
    
    test_RandomUnit()
    test_RandomQuantity()
    test_ConstantFloat()
