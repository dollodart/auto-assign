# Description
The purpose of this is to create a FOSS alternative to homework softwares such as McGraw Hill which is still hardcopy and therefore adequate for higher level courses in which problems are multi-step and partial credit is assigned by human graders. Though computer science departments have developed their own dynamic web apps for homework evaluation (and presumably other departments are, if too slowly, adopting these web apps), this automated hard copy has, as far as I know, no precedent.

It is known that departments, especially for core courses, have large holdings (several hundreds) of problems which they carefully curate and select more or less at random, accounting for difficulty, for assignments. As a further automation of this procedure, it should be possible to define a problem object, which has randomized inputs, other values exceeding the degrees of freedom which are evaluated, and solutions, along with a text prompt, difficulty level, number of points, and so on.

Additional customization for the students, beyond the assignment sheet and solution sheet having the values they used, are in providing notices related to their performance if this is integrated with a package for grading.

    Dear <Student Name>,

    This is assignment 7 of your course in Calculus 2. On your previous assignment you earned <Grade>--this is <+/-> <value> <above/below> the average score. <Well done!/If you are stuck on a particular problem or need help generally for the class, please contact the TA <TA name> at <TA contact information>> 

# Workflow

In a markup language like YAML, define the parts of the problem as a dictionary. All variable names must be defined in this dictionary. One can have either canonical values or NaN or Null.

Define problem objects from these dictionaries.

Make an algorithm which loops through randomly generated values, assigning to the inputs of an instance new values.

Output formatted text for each problem into a latex file and call the system to compile it.

# References
See http://kitchingroup.cheme.cmu.edu/blog/2014/02/03/Using-YAML-in-python-for-structured-data/.

Note the Cheetah template engine can be used rather than the direct formatting done here.
