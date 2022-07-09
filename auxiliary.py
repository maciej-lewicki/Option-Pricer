# Auxiliary functions

# Just to practice decorator's implementation

import time


def execution_time(wrapped_func):
    """ An universal counter of execution time  """

    def inner_func(*args, **kwargs):
        start = time.time()
        output = wrapped_func(*args, **kwargs)
        end = time.time()
        print("Execution time: " + str(end - start))
        return output

    return inner_func


def maximum(n1, n2):
    return n1 if n1 >= n2 else n2
