#access hidden methods by the class name
from quantities import *
from quantities.registry import unit_registry
r = unit_registry._UnitRegistry__Registry
d = r._Registry__shared_state
d = d['_Registry__context']

dim = {}
conv = {}
for k, v in d.items():
    try:
        v = v.simplified
        mag = v.magnitude
        d = {k.symbol:v for k, v in dict(v.dimensionality).items()}
        d = {**d, **{k.name:v for k, v in dict(v.dimensionality).items()}}
        dim[k] = (d['kg'] if 'kg' in d.keys() else 0,
                  d['m'] if 'm' in d.keys() else 0,
                  d['s'] if 's' in d.keys() else 0,
                  d['A'] if 'A' in d.keys() else 0,
                  d['K'] if 'K' in d.keys() else 0,
                  d['cd'] if 'cd' in d.keys() else 0,
                  d['mol'] if 'mol' in d.keys() else 0)
        conv[k] = v.magnitude
    except Exception as e:
        pass

idim = {}
for k, v in dim.items():
    if v not in idim.keys():
        idim[v] = []
    idim[v].append(k)

si7 = 'kg','m','s','A','K','cd','mol'
def dim2si(x):
    st = ''
    for c, i in enumerate(x):
        if i != 0:
            if i == 1:
                st += si7[c] + '*'
            else:
                st += si7[c] + '^' + str(i) + '*'
    return st.rstrip('*')

dim[''] = (0,0,0)
conv[''] = 1

for i in range(-5,5):
    for ii in range(-5,5):
        for iii in range(-5,5):
            x = i, ii, iii,0,0,0,0
            si = dim2si(x)
            dim[si] = x
            conv[si] = 1


#should be defined in the template file for latex specific templates
#def plain2latex(x):

#fundamental units (Temperature -> energy, current -> inverse time)
#fund2name = {(1,0,0): 'Mass',
#        (0,1,0): 'Distance',
#        (0,0,1): 'Time',
#        (0,0,-1): 'Frequency/Number Rate',
#        (0,-1,0): 'Inverse Distance'} #...
