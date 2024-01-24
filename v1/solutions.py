import numpy as np


def solver_00000002(alpha, beta):
    interval = np.linspace(alpha, beta, 20)
    return trapz(interval)


handles = {'00000002': solver_00000002}
