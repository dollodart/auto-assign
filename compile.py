import subprocess
import numpy as np
from Cheetah.Template import Template
from dbprobs import A01


with open('template.cheetah','r') as _:
    tclass = Template.compile(_.read(), baseclass=dict)

# randomly generate subset of problems
A01.rng(3) 

for n in range(1): # number of students
    name_a = f'out/id-{n}.tex'
    name_s = f'out/soln-id-{n}.tex'
    st_a = ''
    st_s = ''
    for prob in A01.subset:
        for var in prob:
            var.rng()
        prob.solve()

    with open(name_a, 'w') as _:
        ass = tclass(assignment_name=A01.title,
                student_id=n,
                problems=A01.subset,
                is_soln=False)
        _.write(ass.respond())

    with open(name_s, 'w') as _:
        soln = tclass(assignment_name=A01.title,
                student_id=n,
                problems=A01.subset,
                is_soln=True)
        _.write(soln.respond())

    subprocess.run(['pdflatex', '-output-directory=out', name_a])
    subprocess.run(['pdflatex', '-output-directory=out', name_s])
