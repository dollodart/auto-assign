header = 'Difficulty={0}\n\nNumber Points={1}'


class problem():
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

    def calculate_from(self, temp):
        e = {}
        d = temp  # this must exist since the evaluation is done in terms of temp
        for key in self.evaluator.keys():
            e[key] = eval(self.evaluator[key])
        for key in self.solver.keys():
            e[key] = eval(self.solver[key])
        self.vals = {**temp, **e}

    def __init__(
            self,
            title,
            statement,
            inputs,
            evaluator,
            solver,
            difficulty,
            points,
            solution,
            references=None):
        self.title = title
        self.statement = statement
        self.inputs = inputs
        self.evaluator = evaluator
        self.solver = solver
        self.difficulty = difficulty
        self.points = points
        self.solution = solution
        self.references = references
        self.dof = len(self.inputs)
        # collect all key-value pairs in one dictionary for formatting
        temp = inputs.copy()
        if references is not None:
            temp = {**temp, **references}
        self.calculate_from(temp)

    def update(self):
        temp = self.inputs.copy()
        if self.references is not None:
            temp = {**temp, **self.references}
        self.calculate_from(temp)

    def format_assignment(self):
        statement = self.statement.format_map(self.vals)
        return r'\subsection{{{2}}}\n\n{0}\n\n{1}'.format(
            header.format(self.difficulty, self.points), statement, self.title)

    def format_solution(self):
        assignment = self.format_assignment()
        solution = self.solution.format_map(self.vals)
        return r'{0}\n\n\subsection{{Solution}}\n\n{1}'.format(
            assignment, solution)

# old example
# def my_evaluator(dct):
#    dct['ratio']=dct['alpha']/dct['beta'] #for problem statement
#    dct['alpha^2']=dct['alpha']**2 #for solution (intermediate values)
#    return dct
# def my_solver(dct):
#    dct['solution']=dct['alpha']**2/dct['beta']
#    return dct

#title='Evaluating a fraction with powers'
# points=10
# difficulty=1
#statement='Given $\\alpha = {alpha:.2f}$ and $\\beta = {beta:.2f}$, evaluate $\\alpha^{{2}}/\\beta.\nHint: $\\alpha/\\beta$ = {ratio:.2f}.'
#solution='The expression evaluates to ${alpha:.2f}^2/{beta:.2f}={alpha:.2f}\\times{alpha:.2f}/{beta:.2f}={alpha^2:.2f}/{beta:.2f}={solution:.2f}$. Consult \\cite{{{ref1}}}.'
# inputs={'alpha':2,'beta':5}
# references={'ref1':'mybibtextrefname'}
# evaluator=my_evaluator
# solver=my_solver
#
#import numpy as np
# inputs=dict(zip(inputs.keys(),np.random.random(len(inputs))))
# my_problem=problem(title,statement,inputs,evaluator,solver,difficulty,points,solution,references)
# print(my_problem.inputs)
# print(my_problem.format_assignment())
# print(my_problem.format_solution())
# print(my_problem.dof)
