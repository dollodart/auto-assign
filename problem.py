import numpy as np
import numpy.random as r
from utils import prec_round

class Assignment():
    """

    Assignment class randomly selects problems, then can randomly
    generate from those selected problems

    """

    def __init__(self 
            , problems
            , title
           #,... other metadata 
            ):
        self.problems = problems # problems is all possible problems
        self.title = title

    def rng(self,num_problems,min_difficulty=0,max_difficulty=100000): 

        self.subset = r.choice(self.problems, 
                num_problems, 
                replace = False) 
        while ( sum(x.points for x in self.subset) > max_difficulty |\
                sum(x.points for x in self.subset) < min_difficulty ):
            self.subset = r.choice(self.problems, 
                    num_problems,
                    replace = False)
        return None

    def __iter__(self):
        for p in self.problems:
            yield p

    def __len__(self):
        return len(self.problems)



class Problem(): 
    """ Class attributes:
    title: Problem title
    points: Number of points the problem is worth
    solution: The unformatted solution text.
    statement: The unformatted (general) problem statement.
    evaluator: Evaluates from randomized inputs intermediate values
    to be presented to the student in the assignment, and in their
    solution. Each subproblem could have a separate evaluator defined
    for it. This is needed because often problem statements overspecify
    a problem (more specifications than degrees of freedom) in order to
    challenge the student.
    solver: Provides only the solution variables that the problem statement asks for directly.
    difficulty: Difficulty on a numerical scale (could be easily changed to have star ratings)
    references: Dictionary of references with key as defined in text format and value as the bibtex reference
    """

    def __init__(
            self,
            title,
            statement,
            difficulty,
            points,
            inputs,
            extraneous_inputs,
            solver,
            solution,
            references=None,
            vspace=6,
            vspace_unit='cm'):

        self.title = title
        self.statement = statement
        self.difficulty = difficulty
        self.points = points
        self.inputs = inputs
        self.extraneous_inputs = extraneous_inputs
        self.solver = solver
        self.solution = solution

        self.references = references
        self.vspace = vspace
        self.vspace_unit = vspace_unit

        self.dof = len(self.inputs)

    def solve(self):
        self.dct = {v.name:v for v in self.inputs}
        soln = self.solver(**self.dct)
        
        for y in soln:
            y.rng()
            self.dct[y.name] = y

        # now add extraneous inputs
        self.dct = {**self.dct,
                **{v.name:v for v in self.extraneous_inputs}}
        return None

    def __iter__(self):
        for v in self.inputs:
            yield v

from unit import dim, idim
from unitparse import eval_units
from quantity import Quantity, eval_dimension, eval_conversion_factor

class RandomSize():
    def __init__(self,
            size):
        self.size = size

    def rng(self):
        value = self.size
        if type(self.size) is tuple:
            if type(self.size[0]) is tuple:
                #value = tuple(r.choice(x for x in self.size))
                x = []
                for tup in self.size:
                    x.append( r.choice(tup) )
                value = tuple(x)
        self.value = value

class ConstantUnit():
    def __init__(self,
            unit,
            dimensionality=None):
        if type(unit) is str:
            unit = eval_units(unit)
        self.value = unit
        self.conversion_factor = 1
        if dimensionality is None:
            self.dimensionality = eval_dimension(self.value)
    def rng(self):
        return None
    def __str__(self):
        return '*'.join(f'{k}({v})' for k, v in self.value.items() if abs(v) > 0)

class RandomUnit(): 
    """ 
    Units should be an iterable, not a set data
    structure (e.g., tuple or list).  The first unit in the provided
    iterable is assumed to the be one which the random or constant variable
    was specified in.
    """

    def __init__(self, unit_set, dimensionality=None): 
        self.unit_set = [eval_units(x) if type(x) is str else x for x in unit_set]
        self.rng()
        if dimensionality is None:
            self.dimensionality = eval_dimension(self.value)

    @classmethod
    def from_unit_dimensionality(cls, unit):
        """Infers dimensionality from unit specified as a string."""

        try:
            d = eval_dimension(eval_units(unit))
            d = dim[d]
        except KeyError:
            pass
        unit_set = idim[d]
        unit_set = sorted(unit_set, key = lambda x: 0 if x == unit else 1)
        
        return cls(unit_set)

    def rng(self):
        self.value = r.choice(self.unit_set)
        self.conversion_factor = eval_conversion_factor(self.unit_set[0])/eval_conversion_factor(self.value)
        # from, to convention

    def __str__(self):
        return '*'.join(f'{k}({v})' for k, v in self.value.items() if abs(v) > 0)


class RandomQuantity:
    """

    It is difficult to implement RandomQuantitty as something other
    than a composite object which makes new instances of quantity on
    randomization if you want to support variable array sizes, since
    numpy arrays do not support element addition and subtraction well.

    """

    def __init__(self, name, lb, ub, size=RandomSize((1,)), unit=ConstantUnit(''), precision=14):
        self.name = name
        self.value = [] # will be deleted in rng
        self.size = size
        self.unit = unit
        self.precision = precision
        self.lb = lb
        self.ub = ub
        self.rng()

    def rng(self):
        self.size.rng()
        self.unit.rng()
        arr = np.random.random(size=self.size.value)*(self.ub - self.lb) + self.lb
        arr *= self.unit.conversion_factor
        arr = prec_round(arr, self.precision)
        del self.value
        self.value = Quantity(arr, self.unit.value)

    def __str__(self):
        return str(np.array(self.value,copy=False))

#greek_lower = 'alpha','beta','gamma','delta',
#greek_upper = 'Gamma','Delta'
class RandomSymbol():
    def __init__(self,
            name,
            symbolset):
        self.name = name
        self.symbolset = symbolset
    def rng(self):
        self.value = r.choice(self.symbolset)
    def __str__(self):
        return self.value


class ConstantVariable():
    def __init__(self,
            name,
            value,
            unit=ConstantUnit('')):
        self.name = name
        self.value = value
        self.unit = unit

    def __str__(self):
        return str(self.value)

class ConstantInteger(ConstantVariable):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def rng(self):
        return None

class ConstantFloat(ConstantVariable):
    def __init__(self,
            name,
            svalue,
            precision=3,
            unit=ConstantUnit('')):
        super().__init__(name,svalue,unit) 
        self.precision = precision
        self.svalue = svalue
        
    def rng(self):
        self.unit.rng() 
        value = self.svalue*self.unit.conversion_factor
        self.value = prec_round(value,precision=self.precision)
        return None


class RandomVariable():
    def __init__(self,
            name,
            lb,
            ub,
            size=None,
            unit=ConstantUnit('')):
        self.name = name
        self.lb = lb
        self.ub = ub
        self.size = RandomSize(size)

    def __str__(self):
        return str(self.value)

class RandomInteger(RandomVariable):
    def __init__(self,
            name,
            lb,
            ub,
            size=None):
        self.size = RandomSize(size)
        self.name = name
        self.lb = lb
        self.ub = ub
        self.rng()

    def rng(self):
        self.size.rng()
        self.value = r.randint(self.lb, self.ub, size=self.size.value)
        return None

class RandomFloat(RandomVariable):
    def __init__(self,
            name,
            lb,
            ub,
            size=None,
            precision=3,
            unit=ConstantUnit('')):
        super().__init__(name,lb,ub,size,unit=unit)
        self.precision = precision
        self.unit = unit

    def rng(self):
        self.unit.rng()
        self.size.rng()
        value = r.random(size=self.size.value)
        value *= self.ub - self.lb
        value += self.lb
        value = value*self.unit.conversion_factor
        self.value = prec_round(value, precision=self.precision)
        return None

if __name__ == '__main__':
    #ru = RandomUnit.from_unit_dimensionality('kg*m^2*s^-2')
    #print(ru.value)
    #print(ru.unit_set)
    #ru.rng()
    #print(ru.value)
    #print(ru.conversion_factor)

    rsize = RandomSize( ((3,4),) )
    runit = RandomUnit(['kg/m','lb/ft','g/cm'])
    rq = RandomQuantity('rq',2,5,rsize,runit,3)
    res = rq.value*rq.value
    print(res)
    rq2 = ConstantFloat('a', rq)
    print(rq2.value)
