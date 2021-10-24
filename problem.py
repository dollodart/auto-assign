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

class ConstantSize():
    def __init__(self,
            size):
        self.size = size
        self.value = self.size

    def rng(self):
        return None

class Unit():
    def __str__(self):
        return '*'.join(f'{k}({v})' for k, v in self.value.items() if abs(v) > 0)

class ConstantUnit(Unit):
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

class RandomUnit(Unit):
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
            d = tuple(d)
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
            value):
        self.name = name
        self.value = value
        try:
            self.size = ConstantSize(len(self.value))
        except TypeError:
            self.size = ConstantSize(1)
            self.value = np.array((self.value,))

    def rng(self):
        return None

    def __str__(self):
        if self.size.value == 0:
            return '\\null'
        elif self.size.value == 1:
            print('value is', self.value)
            return str(self.value[0])
        else:
            return str(self.value)

class ConstantQuantity(ConstantVariable):
    def __init__(self,
            name,
            value,
            precision=3,
            unit=ConstantUnit('')):

        super().__init__(name, value)
        self.precision = precision
        self.unit = unit
        self.value = Quantity(self.value, self.unit.value)

    def rng(self): 
        # if you put in a random unit, you may still want to randomize the unit
        # this is the only randomization among ConstantX classes
        self.unit.rng()
        value = self.value * self.unit.conversion_factor
        value = prec_round(value, self.precision)
        self.value = Quantity(value, self.unit.value)

    def __str__(self):
        if len(self.value) == 0:
            return '\\null'
        elif len(self.value) == 1:
            return str(self.value[0])
        else:
            return str(np.array(self.value,copy=False))

class ConstantInteger(ConstantVariable):
    def __init__(self, name, value):
        super().__init__(name, value)

class ConstantReal(ConstantVariable):
    def __init__(self,
            name,
            value,
            precision=3):
        super().__init__(name, value) 
        self.precision = precision
        self.value = prec_round(self.value, self.precision)

class RandomVariable():
    def __init__(self,
            name,
            lb,
            ub,
            size=None,
            log_uniform = False):
        self.name = name
        self.lb = lb
        self.ub = ub
        if type(size) is tuple:
            self.size = RandomSize(size)
        elif size is None:
            self.size = ConstantSize(1)
        else:
            self.size = size # already a RandomSize or other Size object
        self.log_uniform = log_uniform

    def __str__(self):
        try:
            if len(self.size.value) == 0:
                return '\\null'
            elif len(self.size.value) == 1:
                return str(self.value[0])
            else:
                return str(self.value)
        except TypeError:
            return str(self.value)

    def lin_rng(self):
        return r.random(size=self.size.value)*(self.ub - self.lb) + self.lb

    def log_rng(self):
        return np.exp(r.random(size=self.size.value)*(np.log(self.ub) - np.log(self.lb)) + np.log(self.lb))

    def rng(self):
        self.size.rng()
        if self.log_uniform:
            self.value = self.lin_rng()
        else:
            self.value = self.log_rng()


class RandomInteger(RandomVariable):
    def __init__(self,
            name,
            lb,
            ub,
            size=None,
            log_uniform=False):
        super().__init__(name, lb, ub, size, log_uniform)
        self.rng()

    def rng(self):
        super().rng()
        self.value = np.round(self.value).astype(int)

class RandomReal(RandomVariable):
    def __init__(self,
            name,
            lb,
            ub,
            size=None,
            precision=3,
            log_uniform=False):
        super().__init__(name,lb,ub,size,log_uniform)
        self.precision = precision
        self.rng()

    def rng(self):
        super().rng()
        self.value = prec_round(self.value, precision=self.precision)

class RandomQuantity(RandomVariable):
    """

    It is difficult to implement RandomQuantitty as something other
    than a composite object which makes new instances of quantity on
    randomization if you want to support variable array sizes, since
    numpy arrays do not support element addition and subtraction well.

    """

    def __init__(self, name, lb, ub, size=ConstantSize(1), unit=ConstantUnit(''), precision=14, log_uniform=False):
        super().__init__(name, lb, ub, size, log_uniform)
        self.unit = unit
        self.precision = precision
        self.rng()

    def rng(self):
        super().rng() # note this will set self.value to numpy array, not Quantity
        self.unit.rng()
        value = self.value * self.unit.conversion_factor
        value = prec_round(value, self.precision)
        self.value = Quantity(value, self.unit.value)

    def __str__(self):
        if len(self.value) == 0:
            return '\\null'
        elif len(self.value) == 1:
            return str(self.value[0])
        else:
            return str(np.array(self.value,copy=False))
