import subprocess
from Cheetah.Template import Template
import yaml
import numpy as np
from problem import problem

loader = yaml.Loader
problems = yaml.load(open('db.yaml', 'r'), Loader=loader)

problems = np.random.choice(problems, 3)

ll = []
l = []
for p in problems:
    p = problem(**p)
    a = p.inputs.keys()
    for i in range(10):
        b = np.random.random(p.dof)
        p.inputs = dict(zip(p.inputs.keys(), np.random.random(p.dof)))
        p.update()
        l.append(p.format_assignment())
    ll.append(l)
    l = []

# get the transpose of the above for each students
assignment_number = 1
tclass = Template.compile(
    '\n'.join(
        open(
            'template.cheetah',
            'r').readlines()),
    baseclass=dict)

ll = np.transpose(ll)
for c, row in enumerate(ll):
    val = '\n\n'.join(row)
    fname = 'out/id-{0}.tex'.format(c)
    with open(fname, 'w') as write_file:
        write_file.write(
            tclass(
                assignment_number=assignment_number,
                id=c,
                problems=val).respond())
    subprocess.run(['pdflatex', '-output-directory=out', fname])
