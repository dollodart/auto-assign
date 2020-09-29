# Description 

The purpose of this is to create a FOSS alternative to homework
softwares such as McGraw Hill which is still hardcopy and therefore
suitable for higher level courses in which problems are multi-step and
partial credit is assigned by human graders. Though many departments
have developed their own web apps for homework evaluation, this
automated hard copy has, as far as I know, no precedent.

University departments, especially for core courses, have
large holdings (several hundreds) of problems which they carefully
curate and select more or less at random, accounting for difficulty,
for assignments. As a further automation of assignment generation,
this simple package has been made to create assignments with
randomized inputs and units for each student.

# Design

Because arbitrary problem complexity is desired, there is a problem
class and each problem is defined as a problem object with it's own
solution method. This allows problems which require advanced numerical
techniques to still be solved, while inheriting from the superclass
formatting methods.

Problems are put in assignment containers, as the set of eligible
problems. The assignment has methods for randomly selecting subsets of
these eligible problems subject to some constraints, in this case an
allowed range of cumulative difficulty. The problems randomization is
in its input parameters, which are defined to be in a range of values,
unless a constant. Unit randomization is also supported for both inputs
and outputs.

# TODOs

- Integrate quantities into variables
- Support randomized array dimensions (requires using the autofmt method)
- Support symbolic algebra inputs, outputs, and randomization

## Why not dispatch table the solutions functions and use a text based database format for all other data?

One could use use a dispatch table for solution functions and a simpler
markup language for all other parts of the problem. But even for several
hundred problems loading every problem into memory from the module may
not be rate limiting, rather the solution evaluation for, e.g., problems
involving differential equations may be. In any case if there are memory
or speed limits, the problems and assignments can be split into separate
modules which will not, e.g., weeks 1-3, 3-5, and so on of the semester.

A text based database format would require creating a separate syntax
in addition to the class defintions, which seems like an unnecessary
overhead.

## Why not use templates for the problem statement and solution explanations which are long strings?  

If templates are used for problem statements and solution explanations,
each problem would have its own template which is separately compiled
to allow problems to reuse variable names, and the parameters in the
problem dictionary are directly passed to the Template class instance by
\*\*kwargs.

The motivation to have problems be specified as part of the Problem class
in python string formatting rather than the template engine is two fold:

1. Universal translation to any markup or compiled document language.
2. All data for the problem, including strings which can be searched and
compared, are kept in the Python object.

One could pull data from each problem template, and so not lose any
information and then be able to translate them to other markdown formats
for both of these points. But 

1. Python's native string formatting is already well-developed and
features that templating engines provide inside the text body, such
as defining functions and executing loops, are not necessary for the problem
statement, and could be defined outside the text body in the python
module.

2. Since the markdown or compiling documents are white
space permissive, the awkwardness of long strings in Python can be made
irrelevant by using, e.g., triple quoted with indents. Anyway white
space can be trimmed like is done for docstrings.

