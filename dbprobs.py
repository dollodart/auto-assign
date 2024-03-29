from problem import Assignment, Problem,\
        RandomReal, ConstantReal,\
        RandomInteger, ConstantInteger,\
        RandomUnit, ConstantUnit,\
        RandomSymbol,\
        RandomQuantity, ConstantQuantity

def solver(x,y):
    return ConstantInteger('w',x.value + y.value),

P01 = Problem(title = 'Sum Two Numbers',
        statement = 'Sum the numbers ${x}$ and ${y}$. '
        'Here is another number for fun: ${z}$.',
        difficulty = 'easy',
        points = 2,
        inputs = (RandomInteger('x',1,10),RandomInteger('y',1,10)),
        extraneous_inputs = (RandomInteger('z',-100,100),),
        solver = solver,
        solution = 'The sum of ${x}$ and ${y}$ is ${w}$'
        )

def solver(x,y):
    return ConstantInteger('w',x.value - y.value),

P02 = Problem(title = 'Subtract Two Numbers',
        statement = 'Subtract the number ${y}$ from ${x}$. '
        'Here is another number for fun: ${z}$.',
        difficulty = 'easy',
        points = 2,
        inputs = (RandomInteger('x',1,10),RandomInteger('y',1,10)),
        extraneous_inputs = (RandomInteger('z',-100,100),),
        solver = solver,
        solution = 'The difference of ${x}$ and ${y}$ is ${w}$'
        )

def solver(x,y):
    return ConstantInteger('w',x.value*y.value),

P03 = Problem(title = 'Multiply Two Numbers',
        statement = 'Multiply the numbers ${x}$ and ${y}$. '
        'Here is another number for fun: ${z}$.',
        difficulty = 'easy',
        points = 2,
        inputs = (RandomInteger('x',1,10),RandomInteger('y',1,10)),
        extraneous_inputs = (RandomInteger('z',-100,100),),
        solver = solver,
        solution = 'The product of ${x}$ and ${y}$ is ${w}$'
        )

def solver(x,y):
    return ConstantReal('w', x.value / y.value),

P04 = Problem(title = 'Divide Two Numbers',
        statement = 'Divide the number ${x}$ by ${y}$. '
        'Here is another number for fun: ${z}$.',
        difficulty = 'easy',
        points = 2,
        inputs = (RandomInteger('x',1,10),RandomInteger('y',1,10)),
        extraneous_inputs = (RandomInteger('z',-100,100),),
        solver = solver,
        solution = 'The quotient of ${x}$ and ${y}$ is ${w}$'
        )

from numpy import cumsum
def solver(x):
    return ConstantInteger('w',cumsum(x.value)),

P05 = Problem(title = 'Sum Several Numbers Cumulatively',
        statement = 'Sum the numbers in $${x_autofmt}$$ cumulatively top to bottom.'
        ' The third element of this array is ${x.value[2]}$.',
        difficulty = 'medium',
        points = 4,
        inputs = (RandomInteger('x',1,10,size=((6,8,10),)),), # has randomized size
        extraneous_inputs = tuple(),
        solver=solver,
        solution = 'The cumulative sum is $$\\text{{cumsum}}({x_autofmt}) = {w_autofmt}\,.$$'
        )

def solver(x):
    return ConstantInteger('w',cumsum(x.value,axis=0)),

P06 = Problem(title = 'Sum Along Several Columns Cumulatively',
        statement = 'Sum along the columns in $${x_autofmt}$$ cumulatively top to bottom.'
        ' The element in the second row and third column of this array is ${x.value[1][2]}$.',
        difficulty = 'hard',
        points = 6,
        inputs = (RandomInteger('x',1,10,size=(6,6)),),
        extraneous_inputs = tuple(),
        solver=solver,
        solution = 'The cumulative sum is $$\\text{{cumsum}}({x_autofmt}) = {w_autofmt}\,.$$'
        )

import numpy as np
LENGTH = (0, 1, 0, 0, 0, 0, 0)

def solver(t,g):
    x = g.value*t.value**2/2
    assert (x.dimension == LENGTH).all()
    return ConstantQuantity('x',np.array(x),unit=RandomUnit(('ft','m'))),

P07 = Problem(title = 'Acceleration for an Object Starting at Rest',
        statement = 'An object is released from rest from someones hand at the top of a building.' 
        ' Before it hits the ground, it travels ${t}$ ${t.unit}$.'
        ' How far has it traveled? The local graviational constant is ${g}$ ${g.unit}$',
        difficulty = 'easy',
        points = 2,
        inputs = (RandomQuantity('t',0.5,1.5,precision=3,unit=ConstantUnit('s')),
                  RandomQuantity('g',9.81,9.81,precision=3,unit=ConstantUnit('m*s^-2'))),
        extraneous_inputs = tuple(),
        solver=solver,
        solution= 'After ${t}$ ${t.unit}$ the object has fallen ${x}$ ${x.unit}$.'
        )

def solver(x, y):
    while x.value == y.value:
        x.rng()
    return tuple()

P09 = Problem(title = 'Complete the square',
        statement = 'Complete the square for the expression $$ {x}^2 - 3{x}{y} \,.$$',
        difficulty = 'medium',
        points = 4,
        inputs = (RandomSymbol('x',('x','y','z')),RandomSymbol('y',('x','y','z'))),
        extraneous_inputs = tuple(),
        solver=solver,
        solution = 'The answer is $$({x}-\\frac 32 {y} )^{{2}} - \\frac 34 {y}^2 \,.$$'
        )

def solver(E, G):
    n = E.value/(2*G.value) - 1
    return ConstantQuantity('n', n, unit=ConstantUnit('GPa')),

P10 = Problem(title = 'Evaluate the Poisson\'s ratio',
        statement = 'Evaluate the Poisson\'s ratio for steel with a Young\'s modulus of ${E}$ ${E.unit}$ and shear modulus of ${G}$ ${G.unit}$',
        difficulty = 'easy',
        points = 2,
        inputs = (RandomQuantity('E', 190, 215, precision=3,unit=ConstantUnit('GPa')),
            RandomQuantity('G', 62.4, 79.0, precision=3,unit=ConstantUnit('GPa'))),
        extraneous_inputs = tuple(),
        solver=solver,
        solution = 'The Poisson\'s ratio is $E/(2G) - 1$ = {n}.')

A01 = Assignment( (P01,P02,P03,P04), title='Arithmetic Operations')
A02 = Assignment( (P05,P06), title='Several Arithmetic Operations')
A03 = Assignment( (P07, ), title='Kinematics')
A04 = Assignment( (P09, ), title='Algebra')
A05 = Assignment( (P10, ), title='Statics')
