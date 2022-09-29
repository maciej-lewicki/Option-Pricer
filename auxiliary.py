# Auxiliary functions

import time
import scipy.stats as sc
import numpy as np

def execution_time(wrapped_func):
    """ An universal counter of execution time
    Just to practice decorators
    """

    def inner_func(*args, **kwargs):
        start = time.time()
        output = wrapped_func(*args, **kwargs)
        end = time.time()
        print("Execution time: " + str(end - start))
        return output

    return inner_func


def maximum(n1, n2):
    return n1 if n1 >= n2 else n2


def BoxMullerTrans(sample_size):
        u1 = sc.uniform.rvs(size=sample_size) + 0.000001  # to avoid problems with ln(0)
        u2 = sc.uniform.rvs(size=sample_size)
        return np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)