import os
import numpy as np

n_students = 10
np.random.seed(323)
# seed randomization for reproducible results
x = np.random.random(n_students) * 1.5 + 32.
y = np.random.random(n_students) * 3.2 + 63.
inputs = [x, y]


def evaluator(inputs):
    """
    Evaluates from randomized inputs intermediate values to be presented
    to the student in the assignment. Each subproblem could have a
    separate evaluator defined for it. This is needed because often
    problem statements overspecify a problem (more specifications than
    degrees of freedom) in order to challenge the student.
    """
    return [sum(inputs)]


vrs = inputs + outputs
vrs_names = ['x', 'y', 'z']
dct = dict(zip(vrs_names, vrs))

# creating customized student assignments
for i in range(n_students):
    st = ''
    for n in vrs_names:
        st += r'\def' + '\\' + n + \
            r'{' + '{0:.4f}'.format(dct[n][i]) + r'}' + '\n'
    o_file = 'custom/out-{0}.tex'.format(i)
    with open(o_file, 'w') as write_file:
        write_file.write(st)
    os.system('cat template.tex >> ' + o_file)
    os.system('pdflatex -output-directory=custom ' + o_file)
