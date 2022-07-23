# The code is inspired (loosely) by "Numerical Methods in Finance with C++", M.Capiński & T. Zastawniak, Cambridge Press

# The roadmap proposed in the book:
# Approximate the Black–Scholes price by the CRR price.
# How about path-dependent options? A barrier option? An Asian option?
# Compute the hedging portfolio on top of the price.
# Compute the price from the Black–Scholes formula.
# Include a Monte Carlo pricer.

# Time: 15.05h
# Section: Chp 4
# Page: 75

# TODO (generally in the project):
# 1. Figure out a hook-up with GitHub
# 2. Implement Eur Option pricer using BS formula
# 3. Implement own solvers (to challenge myself)
# 4. Implied volatility calculator

# x. Improvements in option classes
# x. Install numpy (watch out on dependency hell)
# x. Refactor lists to numpy objects

# 'Main' class

import Options as opt
import Binomial as bn
import BlackScholes as bs

if __name__ == "__main__":

    print('\nCall inputs')
    call = opt.Call()
    print('\nPut inputs')
    put = opt.Put()

    print('\nBinomial tree inputs')
    binomial = bn.BinomialModel()

    print('\nBlack-Scholes inputs')
    bsm = bs.BLackScholes()

    print('\nCall:')
    print('EurOpt:' + str(call.calculateOptionPriceCRR(binomial, 'iterative')))
    print("\n")
    print('AmOpt: ' + str(call.calculateOptionPriceBySnell(binomial)))
    print("\n")
    print('AmOpt (BS approx): ' + str(call.approximateBlackScholes(bsm)))

    print('\nPut:')
    print('EurOpt:' + str(put.calculateOptionPriceCRR(binomial, 'iterative')))
    print("\n")
    print('AmOpt: ' + str(put.calculateOptionPriceBySnell(binomial)))
    print("\n")
    print('AmOpt (BS approx): ' + str(put.approximateBlackScholes(bsm)))