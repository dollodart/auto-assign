import subprocess
import numpy as np
from Cheetah.Template import Template

with open('template.cheetah','r') as _:
    tclass = Template.compile(_.read(), baseclass=dict)

def output2latex(assignment, number_students):
    names = []
    for n in range(number_students): # number of students
        name_a = f'out/id-{n}.tex'
        name_s = f'out/soln-id-{n}.tex'
        st_a = ''
        st_s = ''
        for prob in assignment.subset:
            for var in prob:
                var.rng()
            prob.solve()

        with open(name_a, 'w') as _:
            ass = tclass(assignment_name=assignment.title,
                    student_id=n,
                    problems=assignment.subset,
                    is_soln=False)
            _.write(ass.respond())

        with open(name_s, 'w') as _:
            soln = tclass(assignment_name=assignment.title,
                    student_id=n,
                    problems=assignment.subset,
                    is_soln=True)
            _.write(soln.respond())

    names.append(name_a)
    names.append(name_s)
    return names

def latex2pdf(filenames):
    for file in filenames:
        subprocess.run(['pdflatex', '-output-directory=out', file])

def output2pdf(assignment, number_students):
    filenames = output2latex(assignment, number_students)
    latex2pdf(filenames)

if __name__ == '__main__':
    from dbprobs import A01
    # randomly generate possible subset of problems
    A01.rng(len(A01)) 
    output2pdf(A01, 1)
