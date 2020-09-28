import numpy as np
import numpy.random as r
from quantities import Quantity 
from quantities.quantity import get_conversion_factor

class Assignment():
    """

    Assignment class randomly selects problems, then can randomly generate from those selected problems

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
        soln = self.solver(**{k:v.value for k, v in self.dct.items()})
        
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

def prec_round(a, precision=2):
    if a == 0:
        return a
    else:
        s = 1 if a > 0 else -1
        m = np.log10(s * a) // 1
        c = np.log10(s * a) % 1
    return s * np.round(10**c, precision) * 10**m

prec_round = np.vectorize(prec_round)
#def meas_prec(a):
#    """there isn't actually a way to measure/infer specified precision, since 10. and 10.0 are the same input"""
#    a = str(a)
#    a = str(a).replace('.','').strip('0')
#    return len(a)

class ConstantUnit():
    def __init__(self,
            unit):
        self.value = unit
        self.conversion_factor = 1
    def rng(self):
        return None
    def __str__(self):
        return Quantity(1,self.value).dimensionality.latex
    def __repr__(self):
        return self.__str__()

class RandomUnit():
    """Units should be an iterable, not a set data structure (e.g., tuple or list)."""
    def __init__(self,
            unit_set):
        self.unit_set = unit_set
        self.value = self.unit_set[0]

#    @classmethod
#    def from_dimensionality(cls, dimensionality):
#        #look up all units for that dimensionality
#        #... 
#        #ensure the SI unit is the first one given, since this is assumed the value 
#        return cls(unit_set)

    def rng(self):
        self.value = r.choice(self.unit_set)
        self.conversion_factor = get_conversion_factor(Quantity(1,self.unit_set[0]), Quantity(1,self.value))
        # from, to convention
        # the float range is specified in the first unit provided in the unit "set" (where order actually matters)

    def __str__(self):
        return Quantity(1,self.value).dimensionality.latex

    def __repr__(self):
        return self.__str__()

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
            unit=RandomUnit(('',))):
        self.name = name
        self.lb = lb
        self.ub = ub
        self.size = size
    def __str__(self):
        return str(self.value)

class RandomInteger(RandomVariable):
    def rng(self):
        self.value = r.randint(self.lb, self.ub, size=self.size)
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
        value = r.random(size=self.size)
        value *= self.ub - self.lb
        value += self.lb
        value = value*self.unit.conversion_factor
        self.value = prec_round(value, precision=self.precision)
        return None
