from problem import Assignment, Problem, Float, Integer
# there is a subtle difference between init setting and having the variable be set in the class definition
# all solvers must return iterables
# the order of outputs strings must match the order the solver outputs
# (it would also be possible to just define the solver to return a dictionary)

def solver(x,y):
    return x + y,

P01 = Problem(title = 'Sum Two Numbers',
        statement = 'Sum the numbers {x} and {y}. '
        'Here is another number for fun: {z}.',
        difficulty = 'easy',
        points = 2,
        inputs = (Integer('x',1,10),Integer('y',1,10)),
        extraneous_inputs = (Integer('z',-100,100),),
        solver = solver,
        outputs = ('w',),
        solution = 'The sum of {x} and {y} is {w}'
        )

def solver(x,y):
    return x - y,

P02 = Problem(title = 'Subtract Two Numbers',
        statement = 'Subtract the number {y} from {x}. '
        'Here is another number for fun: {z}.',
        difficulty = 'easy',
        points = 2,
        inputs = (Integer('x',1,10),Integer('y',1,10)),
        extraneous_inputs = (Integer('z',-100,100),),
        solver = solver,
        outputs = ('w',),
        solution = 'The difference of {x} and {y} is {w}'
        )

def solver(x,y):
    return x*y,

P03 = Problem(title = 'Multiply Two Numbers',
        statement = 'Multiply the numbers {x} and {y}. '
        'Here is another number for fun: {z}.',
        difficulty = 'easy',
        points = 2,
        inputs = (Integer('x',1,10),Integer('y',1,10)),
        extraneous_inputs = (Integer('z',-100,100),),
        solver = solver,
        outputs = ('w',),
        solution = 'The product of {x} and {y} is {w}'
        )

def solver(x,y):
    return x / y,

P04 = Problem(title = 'Divide Two Numbers',
        statement = 'Divide the number {x} by {y}. '
        'Here is another number for fun: {z}.',
        difficulty = 'easy',
        points = 2,
        inputs = (Integer('x',1,10),Integer('y',1,10)),
        extraneous_inputs = (Integer('z',-100,100),),
        solver = solver,
        outputs = ('w',),
        solution = 'The quotient of {x} and {y} is {w}'
        )

A01 = Assignment( (P01,P02,P03,P04), title='Arithmetic Operations')
