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

if __name__ == '__main__':
    test_all_assignments()
    test_all_problems()
    test_all_output2latex()
