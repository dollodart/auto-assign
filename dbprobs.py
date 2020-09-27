from problem import Assignment, Problem, Float, Integer, Constant, Unit
# there is a subtle difference between init setting and having the variable be set in the class definition
# all solvers must return iterables
# the order of outputs strings must match the order the solver outputs
# (it would also be possible to just define the solver to return a dictionary)

def solver(x,y):
    return x + y,

P01 = Problem(title = 'Sum Two Numbers',
        statement = 'Sum the numbers ${x.value}$ and ${y.value}$. '
        'Here is another number for fun: ${z.value}$.',
        difficulty = 'easy',
        points = 2,
        inputs = (Integer('x',1,10),Integer('y',1,10)),
        extraneous_inputs = (Integer('z',-100,100),),
        solver = solver,
        outputs = ('w',),
        solution = 'The sum of ${x.value}$ and ${y.value}$ is ${w.value}$'
        )

def solver(x,y):
    return x - y,

P02 = Problem(title = 'Subtract Two Numbers',
        statement = 'Subtract the number ${y.value}$ from ${x.value}$. '
        'Here is another number for fun: ${z.value}$.',
        difficulty = 'easy',
        points = 2,
        inputs = (Integer('x',1,10),Integer('y',1,10)),
        extraneous_inputs = (Integer('z',-100,100),),
        solver = solver,
        outputs = ('w',),
        solution = 'The difference of ${x.value}$ and ${y.value}$ is ${w.value}$'
        )

def solver(x,y):
    return x*y,

P03 = Problem(title = 'Multiply Two Numbers',
        statement = 'Multiply the numbers ${x.value}$ and ${y.value}$. '
        'Here is another number for fun: ${z.value}$.',
        difficulty = 'easy',
        points = 2,
        inputs = (Integer('x',1,10),Integer('y',1,10)),
        extraneous_inputs = (Integer('z',-100,100),),
        solver = solver,
        outputs = ('w',),
        solution = 'The product of ${x.value}$ and ${y.value}$ is ${w.value}$'
        )

def solver(x,y):
    return x / y,

P04 = Problem(title = 'Divide Two Numbers',
        statement = 'Divide the number ${x.value}$ by ${y.value}$. '
        'Here is another number for fun: ${z.value}$.',
        difficulty = 'easy',
        points = 2,
        inputs = (Integer('x',1,10),Integer('y',1,10)),
        extraneous_inputs = (Integer('z',-100,100),),
        solver = solver,
        outputs = ('w',),
        solution = 'The quotient of ${x.value}$ and ${y.value}$ is ${w.value}$'
        )

from numpy import cumsum
def solver(x):
    return cumsum(x),

P05 = Problem(title = 'Sum Several Numbers Cumulatively',
        statement = 'Sum the numbers in $${x_autofmt}$$ cumulatively top to bottom.'
        ' The third element of this array is ${x.value[2]}$.',
        difficulty = 'medium',
        points = 4,
        inputs = (Integer('x',1,10,size=6),),
        extraneous_inputs = tuple(),
        solver=solver,
        outputs= ('w',),
        solution = 'The cumulative sum is $$\\text{{cumsum}}({x_autofmt}) = {w_autofmt}\,.$$'
        )

def solver(x):
    return cumsum(x,axis=0),

P06 = Problem(title = 'Sum Along Several Columns Cumulatively',
        statement = 'Sum along the columns in $${x_autofmt}$$ cumulatively top to bottom.'
        ' The element in the second row and third column of this array is ${x.value[1][2]}$.',
        difficulty = 'hard',
        points = 6,
        inputs = (Integer('x',1,10,size=(6,6)),),
        extraneous_inputs = tuple(),
        solver=solver,
        outputs = ('w',),
        solution = 'The cumulative sum is $$\\text{{cumsum}}({x_autofmt}) = {w_autofmt}\,.$$'
        )

def solver(t,g):
    x = g*t**2/2
    return '{:.3E}'.format(x),

P07 = Problem(title = 'Acceleration for an Object Starting at Rest',
        statement = 'An object is released from rest from someones hand at the top of a building.' 
        ' Before it hits the ground, it travels ${t.value}$ {t.unit.value}.'
        ' How far has it traveled? The local graviational constant is ${g.value}$ {g.unit.value}',
        difficulty = 'easy',
        points = 2,
        inputs = (Float('t',0.5,1.5,unit=Unit(('s',))), Constant('g',9.81,Unit(('m/s**2',)))),
        extraneous_inputs = tuple(),
        solver=solver,
        outputs=('x',),
        solution= 'After ${t.value}$ {t.unit.value} the object has fallen ${x.value}$ meters.'
        )
#A01 = Assignment( (P01,P02,P03,P04), title='Arithmetic Operations')
A01 = Assignment( (P05,P06,P07), title='Several Arithmetic Operations')
