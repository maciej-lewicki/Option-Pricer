# The code is inspired (loosely) by "Numerical Methods in Finance with C++", M.Capiński & T. Zastawniak, Cambridge Press

# The roadmap proposed in the book:
# Approximate the Black–Scholes price by the CRR price.
# How about path-dependent options? A barrier option? An Asian option?
# Compute the hedging portfolio on top of the price.
# Compute the price from the Black–Scholes formula.
# Include a Monte Carlo pricer.
# Path-dependent and Basket options
# PDEs and finite difference methods

# Time: 21.30h + 10.30
# Section: Chp 5.4
# Page: 103

# TODO (generally in the project):
# 0. Commit all changes, set out a new branch.
# Design:
# 1. Refactor Options structure, e.g. wrt path-dependent options
# 2. Improvements in option classes (TODOs)
# (Remote repo)
# Refactoring:
# 3. Improve functions logic
# 4. Numpy: use more numpy, replace for loops by built-ins, use vectorization
# (Remote repo)
# Greeks:
# 6. Greeks using FD
# 7. Greeks using MC
# 8. Variance reduction
# (Remote repo)

# Later:
# x. Improve documentation strings
# x. Compare with another available quant library (e.g. QuantLib)

# 'Main' class

import Options as opt
import Binomial as bn
import PricingModels as bs
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    print('\nCall inputs')
    call = opt.Call()
    # print('\nPut inputs')
    # put = opt.Put()

    # print('\nBinomial tree inputs')
    # binomial = bn.BinomialModel()

    print('\nBlack-Scholes inputs')
    bsm = bs.BlackScholes()
    num_samples = 10000

    print('\nCall:')
    # print('EurOpt:' + str(call.calculateOptionPriceCRR(binomial, 'iterative')))
    # print("\n")
    # print('AmOpt: ' + str(call.calculateOptionPriceBySnell(binomial)))
    # print("\n")
    # print('AmOpt (BS approx): ' + str(call.approximateBS(bsm)))
    print('EurOpt:' + str(call.calculateOptionPriceBSM(bsm)))
    # print('AsianOpt:' + str(call.calculateAsianOptMC(bsm, num_samples)))
    print('EurOpt MC:' + str(call.calculateEurOptMC(bsm, num_samples)))
    print('Pricing error:' + str(call.pricing_error))

    print('\nPut:')
    # print('EurOpt:' + str(put.calculateOptionPriceCRR(binomial, 'iterative')))
    # print("\n")
    # print('AmOpt: ' + str(put.calculateOptionPriceBySnell(binomial)))
    # print("\n")
    # print('AmOpt (BS approx): ' + str(put.approximateBS(bsm)))
    # print('EurOpt:' + str(put.calculateOptionPriceBSM(bsm)))
    # print('AsianOpt:' + str(put.calculateAsianOptMC(bsm, num_samples)))

    # sample_size = 1000
    # T = 1
    # S0 = 100
    # path = bsm.generateSamplePath(T, sample_size, S0)
    # x = np.linspace(0, T, sample_size)
    # plt.plot(x, path)
    # plt.show()
