import subprocess
import numpy as np
from Cheetah.Template import Template
from dbprobs import A01

probs = A01.rng(3) # 3 problems

with open('template.cheetah','r') as _:
    tclass = Template.compile(_.read(), baseclass=dict)

for n in range(3): # number of students
    name_a = f'out/id-{n}.tex'
    name_s = f'out/soln-id-{n}.tex'
    st_a = ''
    st_s = ''
    for prob in probs:
        prob.rng()
#        st_a += prob.format_assignment()
#        st_s += prob.format_solution()

    with open(name_a, 'w') as _:
        ass = tclass(assignment_name=A01.title,
                student_id=n,
                problems=probs,
                is_soln=False)
        _.write(ass.respond())

    with open(name_s, 'w') as _:
        soln = tclass(assignment_name=A01.title,
                student_id=n,
                problems=probs,
                is_soln=True)
        _.write(soln.respond())

    subprocess.run(['pdflatex', '-output-directory=out', name_a])
    subprocess.run(['pdflatex', '-output-directory=out', name_s])
