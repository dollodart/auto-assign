"""
Very indirect way of obtaining a datatable of units, owing to some
difficulty with the UnitRegistry object in the quantities package.

You can print the object __context object, but I wasn't able
to pickle it due to threadlock. Maybe assign it a global variable name and export it some otherway.
"""

compound_dimensions = ['acceleration', 'angle', 'area', 'compound', 'concentration', 
        'dimensionless', 'electromagnetism', 'energy', 'force', 
        'frequency', 'heat', 'information', 'length', 'mass', 
        'power', 'prefixes', 'pressure', 'radiation', 'substance', 
        'temperature', 'time', 'velocity', 'viscosity', 'volume']

base = 'quantities.units'
po2dim = {1: 'mass',
     2: 'length',
     3: 'time',
     4: 'current',
     5: 'luminous_intensity',
     6: 'substance',
     7: 'temperature',
     8: 'information',
     9: 'currency',
     90: 'unknown',
     99: 'compound'}

intkeys = po2dim.keys()
import pandas as pd
df = []

primes = {'dimensionless':1,
        'kg':2,
        'invkg':3,
        'm':5,
        'invm':7,
        's':11,
        'invs':13,
        'A':17,
        'invA':19,
        #luminous intensity:?
        #inv luminous intensity:?
        'mol':23,
        'invmol':31,
        'K':37,
        'invK':41,
        'bit':43,
        'invbit':47
        }

def pfactor(x):
    length = mass = time = substance = \
            temperature = current = \
            luminuous_intensity = information\
            = currency = 0
    for i in 2,3,5,7,11,13,17,19,23,31,37,41,43,47:
        while x % i == 0 and x > 1:
            x /= i
            if i == 2:
                mass += 1
            if i == 3:
                mass -= 1
            if i == 5:
                length += 1
            if i == 7:
                length -= 1
            if i == 11:
                time += 1
            if i == 13:
                time -= 1
            if i == 17:
                currency += 1
            if i == 19:
                currency -= 1
            if i == 23:
                substance += 1
            if i == 31:
                substance -= 1
            if i == 37:
                temperature += 1
            if i == 41:
                temperature -= 1
            if i == 43:
                information += 1
            if i == 47:
                information -= 1
    return mass, length, time, current, \
            luminuous_intensity, substance, temperature, currency

def infer_dimensionality(simplified_quantity):
    """In the absence of symbolic algebra, or a natural
    language math parser, for inputs of a simple type, prime factorize a
    multiplication problem to find counts of units."""

    unit = str(simplified_quantity).split(' ')[1]
    unit = unit.replace('/', '*inv')
    if 'inv(' in unit:
        unit = unit.rstrip(')').split('(')
        unit[1] = (unit[1].replace('**','^')
                ).replace('*','*inv').replace('^','**')
        unit = ''.join(unit)

    dimn = eval(unit, primes) 
    dim = pfactor(dimn)
    return dim 

def dim2siunit(dim):
    sis = ('kg','m','s','A','?','mol','K','$')
    return '*'.join(f'{sis[i]}^{c}' for i, c in enumerate(dim) if c != 0)

for cd in compound_dimensions:
    module = base + '.' + cd
    mod = __import__(module)
    for unit_name, unit_obj in mod.__dict__.items():
        if 'unitquantity' in str(type(unit_obj)):
            po = unit_obj._primary_order
            cr = unit_obj._conv_ref
            if (cr is not None and po in intkeys):
                if po == 99 or 90:
                    dim = infer_dimensionality(cr)
                    fundamental_dim = (dim[0] + dim[6], 
                            dim[1] + dim[6]*2,
                            dim[2] - dim[6]*2 - dim[3])
                    # temperature -> energy, current -> inverse time
                else:
                    dim = [0,0,0,0,0,0,0,0,0]
                    fundamental_dim = [0,0,0]
                    dim[po] = 1
                    if po < 3:
                        fundamental_dim[po] += 1

                df.append((dim, fundamental_dim, unit_name, float(cr.magnitude)))

df = pd.DataFrame(df, 
        columns=['dimension', 'fundamental dimension', 'unit', 'si conversion']).drop_duplicates()
