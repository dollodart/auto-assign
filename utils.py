import numpy as np
def prec_round(a, precision=2):
    if a == 0:
        return a
    else:
        s = 1 if a > 0 else -1
        m = np.log10(s * a) // 1
        c = np.log10(s * a) % 1
    return s * np.round(10**c, precision) * 10**m

prec_round = np.vectorize(prec_round)
