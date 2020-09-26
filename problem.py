import numpy.random as r

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
        return self.subset



class Problem():
    """
    Class attributes:

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
            outputs,
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
        self.outputs = outputs
        self.solver = solver
        self.solution = solution

        self.references = references
        self.vspace = vspace
        self.vspace_unit = vspace_unit

        self.dof = len(self.inputs)

    def rng(self):
        self.dct = {v.name:v.rng() for v in self.inputs}
        soln = self.solver(**self.dct)
        
        for c, y in enumerate(soln):
            self.dct[self.outputs[c]] = y

        # now add extraneous inputs
        self.dct = {**self.dct,
                **{v.name:v.rng() for v in self.extraneous_inputs}}
        return self.dct

class Constant():
    def __init__(self,
            name,
            value):
        self.name = name
        self.value = value
    def rng(self):
        return self.value

class Variable():
    def __init__(self,
            name,
            lb,
            ub,
            size=None):
        self.name = name
        self.lb = lb
        self.ub = ub
        self.size = size

class Integer(Variable):
    def rng(self):
        self.value = r.randint(self.lb, self.ub, size=self.size)
        return self.value

class Float(Variable):
    def __init__(self,
            name,
            lb,
            ub,
            size=None,
            precision=3):
        super().__init__(name,lb,ub,size)
        self.precision = precision

    def rng(self):
        self.value = round(r.random(size=self.size), self.precision)*(self.ub - self.lb) + self.lb
        return self.value
