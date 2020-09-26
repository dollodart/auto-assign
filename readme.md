# Description 

The purpose of this is to create a FOSS alternative to
homework softwares such as McGraw Hill which is still hardcopy and
therefore suitable for higher level courses in which problems are
multi-step and partial credit is assigned by human graders. Though
computer science departments have developed their own dynamic web apps
for homework evaluation (and presumably other departments are, if too
slowly, adopting these web apps), this automated hard copy has, as far
as I know, no precedent.

It is known that departments, especially for core courses, have large
holdings (several hundreds) of problems which they carefully curate
and select more or less at random, accounting for difficulty, for
assignments. As a further automation of assignment generation, this simple package 
has been made to define a problem object, which has randomized inputs,
other values exceeding the degrees of freedom which are evaluated, and
solutions, along with a text prompt, difficulty level, number of points,
and so on.

Additional customization for the students, beyond the assignment sheet
and solution sheet having the values they used, are in providing notices
related to their performance if this is integrated with a package for
grading.

# Design

Because arbitrary problem complexity is desired, there is a problem
class and each problem is defined as a problem object with it's own
solution method. This allows problems which require advanced numerical
techniques to still be solved, while inheriting from the superclass
formatting methods.

Problems are put in assignment containers, as the set of eligible
problems. The assignment has methods for randomly selecting subsets of
these eligible problems subject to some constraints, in this case an
allowed range of cumulative difficulty.

More elegant solutions which may use a dispatch table for solution
functions and a simpler text based markup language for all other parts
of the problem. However even for several hundred problems loading every
problem into memory from the module may not be rate limiting, rather the 
solution evaluation for, e.g., problems involving differential equations may be.
