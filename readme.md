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
and outputs, and symbol randomization for algebra or analytical solutions.

# Implementation of Dimensioned Quantities

There are at least two packages, the python-quantities package and
brian2 packages, that support unit specification and calculating with
dimensioned quantities. The python-quantities package relies on python's
built-in `eval` to evaluate arbitrary unit specification strings,
while the brian2 package has its own parser and compiler which is also
developed for reading plaintext equation specifications. Both of these
packages implement subclasses of numpy arrays which have redefined
ufuncs to also calculate the units and dimensionality for composite
objects or attributes of the subclass with the same magic methods
corresponding to infix notation such as arithmetic (+-\*/), power
(\*\*), and matrix multiplication (@). Note that while python-quantities
conflates dimension (such as length and mass) with unit (such as meter
and kilogram), brian2 has separate Dimension, Unit, and Quantity
objects.

In fact, though a computational nueroscience package, the largest
non-computer generated and non-test file by line count is the
brian2.units.fundamentalunits module at 2491. The differential equation
solutions are, when not explicit solvers (next matrix is matrix
multiplication on previous matrix), from the GNU scientific library.

To use these classes, it is just a matter of defining subclasses or
composite objects which have randomization methods. What is done here
is a simpler implementation of the brian2 quantity in which units
are dictionaries and dimensions are 7 element numpy arrays, and unit
conversions are achieved just by using a reference dictionary of
units. Since brian2 has little unit support, only metric prefixes on SI
units, the unit registry from python-quantities is used.

In fact, I found another package, ChemPy by Bjorn Dahlgren, that defines
an ArithmeticDict which is very similar to the solution given here for
dealing with quantities.

# TODOs

- Refactor objects to remove redundancies and unnecessary
classes. In particular Constant quantities may not be needed for solver outputs.
- Improve automatic white space creation, tex primitives/latex macros or
document layout package geometry
- Support HTML output with hidden identifiers of correct/incorrect
solution, possible javascript output for evaluation
- Support 2-D arrays for quantities 
- As seen in the below discussion on templating, it isn't clear that the
given "general markdown" method is satisfactory. One problem is that one
cannot nest mathematical environments in LaTeX, so either the templating
enging has to be aware of that and change delimiters for substituted
values, or the user has to be TeX aware and use the amsmath \text macro
to allow regular and mathematical text nesting.

## Why not dispatch table the solutions functions and use a text based database format for all other data?

One could use use a dispatch table for solution functions and a simpler
markup language for all other parts of the problem. But even for several
hundred problems loading every problem into memory from the module may
not be what takes the most time, rather the solution evaluation for,
e.g., problems involving differential equations may be. In any case if
there are memory or speed limits, the problems and assignments can be
split into separate modules which will not, e.g., weeks 1-3, 3-5, and so
on of the semester.

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

1. Python's standard library string formatting is already well-developed and
features that templating engines provide inside the text body, such
as defining functions and executing loops, are not necessary for the
problem statement, and could be defined outside the text body in the
python module.

2. Since the markdown or compiling documents are white
space permissive, the awkwardness of long strings in Python can be made
irrelevant by using, e.g., triple quoted with indents. Anyway white
space can be trimmed like is done for docstrings.

The first motivation is actually weak, since it would in effect require
defining a new markup, or to have many classes which don't just
represent variables but also their formatting in the text body, like
InlineEquation. The template documents would then have to have either
markup converters (string manipulation) or type-inspecting formats,
e.g., 

```
#from problem import InlineEquation
#if type(A) == InlineEquation
#...
#end if
```

But already there are markup converters. The second motivation, standing alone,
is weak because it is possible to parse the problem statements from the
templates provided they exist. Finally, Tex is the best native format, since it
has the richest selection of in-line mathematical typesetting--web renderes
just borrow Tex formatting with a javascript package MathJax, which has only a
subset of macros available in LaTeX distributions, though the most often used
and important ones in amsmath.

# Other references

I found that E.L.F. Software, ran by John Kormylo, developed batch creation of
mathematics worksheets similar to this. Because it only uses TeX/LaTeX, it is
far less general.

# TODOs

- Make a consistent class structure and polymorphism for random and constant objects
- Consistently define dimensions as either mutable arrays or immutable tuples.
  some of the Quantity methods require them to be mutable arrays but to use
  them as hashable objects in a dictionary requires them to be immutable tuples
