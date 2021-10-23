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
        d = {k.symbol.lower():v for k, v in dict(v.dimensionality).items()}
        d = {**d, **{k.name.lower():v for k, v in dict(v.dimensionality).items()}}
        dim[k] = (d['kg'] if 'kg' in d.keys() else 0,
                  d['m'] if 'm' in d.keys() else 0,
                  d['s'] if 's' in d.keys() else 0,
                  d['A'] if 'A' in d.keys() else 0,
                  d['K'] if 'K' in d.keys() else 0,
                  d['cd'] if 'cd' in d.keys() else 0,
                  d['mol'] if 'mol' in d.keys() else 0)
        dim[k] = tuple(int(x) for x in dim[k])
        conv[k] = float(v.magnitude)
    except Exception as e:
        pass

idim = {}
for k, v in dim.items():
    if v not in idim.keys():
        idim[v] = []
    idim[v].append(k)

# for hashable types
for k in idim:
    idim[k] = tuple(idim[k])
