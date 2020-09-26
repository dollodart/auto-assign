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
        #todo: support rng under constraint, e.g., minimum cumulative difficulty
        s = r.choice(self.problems, num_problems, replace = False) 
        while ( sum(x.points for x in s) > max_difficulty | sum(x.points for x in s) < min_difficulty ):
            s = r.choice(self.problems, num_problems, replace = False)
        return s



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

    header = 'Difficulty={0}\n\nNumber Points={1}'

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
            references=None):

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

        self.dof = len(self.inputs)

    def rng(self):
        self.dct = {v.name:v.rng() for v in self.inputs}
        soln = self.solver(**self.dct)
        
        for c, y in enumerate(soln):
            self.dct[self.outputs[c]] = y

        # now add extraneous inputs
        self.dct = {**self.dct,**{v.name:v.rng() for v in self.extraneous_inputs}}

    def format_assignment(self):
        statement = self.statement.format_map(self.dct)
        return '\subsection{{{2}}}\n\n{0}\n\n{1}'.format(
            self.header.format(self.difficulty, self.points), statement, self.title)

    def format_solution(self):
        assignment = self.format_assignment()
        solution = self.solution.format_map(self.dct)
        return '{0}\n\n\subsubsection{{Solution}}\n\n{1}'.format(
            assignment, solution)

class Variable():
    def __init__(self,
            name,
            lb,
            ub,
            size=None):
        self.name = name
        self.lb = lb
        self.ub = ub
        self.size = None

class Integer(Variable):
    def rng(self):
        return r.randint(self.lb, self.ub, size=self.size)

class Float(Variable):
    def rng(self):
        return r.random(size=self.size)*(self.ub - self.lb) + self.lb
