# Options container class

from abc import ABC, abstractmethod
import math
import auxiliary as aux
import Binomial as bn
import numpy as np
import scipy.stats as sc


class Options(ABC):
    """ Options class container
    we apply ABC class/module to create abstract methods """
    def __init__(self):
        self.time_to_maturity = int(input("Pass time to expiration (in years): "))
        self.num_intervals = int(input("Pass number of intervals: "))
        while self.num_intervals < 0 or self.time_to_maturity < 0:
            print("Number of intervals (N) should be higher than 0, the same for time to maturity (T)")
            self.time_to_maturity = int(input("Pass time to maturity: "))
            self.num_intervals = int(input("Pass number of intervals: "))
        self.h = float(self.time_to_maturity / self.num_intervals)

        self.st = float(input("Pass initial underlying price: "))
        while self.st < 0:
            self.st = float(input("St should be non-negative number. Try again: "))

    @abstractmethod
    def payoff(self, price):
        """ it's shared by two derived classes - Call and Put"""
        pass


class EurOpt(Options):
    """ European Options """

    @aux.execution_time
    def calculateOptionPriceCRR(self, binmodel, method='iterative'):
        """ Simple option pricer using binomial tree and (Cox-Ross-Rubinstein) formula. """

        # TODO: Add safeguard/exception handler on too big input because of factorial function explodes quickly
        final_price = -1
        if method == 'iterative':
            m = self.num_intervals - 1  # intermediate steps
            price = []
            for i in range(self.num_intervals + 1):  # including n
                price.append(self.payoff(binmodel.calculateStockPriceBinominal(self.st, self.num_intervals, i)))
            while m >= 0:
                for i in range(m+1):
                    price[i] = (binmodel.q*price[i+1]+(1-binmodel.q)*price[i])/(1+binmodel.r)
                m -= 1
            final_price = price[0]
        elif method == 'aggregated':
            final_price = math.factorial(self.num_intervals) / pow((1 + binmodel.r), self.num_intervals) \
                          * sum((1 / (math.factorial(i) * math.factorial(self.num_intervals - i)) * pow(binmodel.q, i)
                                 * pow(1 - binmodel.q, self.num_intervals - i)
                                 * self.payoff(binmodel.calculateStockPriceBinominal(self.st, self.num_intervals, i))
                                 for i in range(self.num_intervals + 1)))  # including n, generator is enough
            # TODO: check the alternative solution with condition checking embedded in the index (Hull, p. 298)
        else:
            print('Wrong method name - try again with iterative or aggregated')
        return final_price


class AmOpt(Options):
    """ American Options """

    @aux.execution_time
    def calculateOptionPriceBySnell(self, binmodel):
        """ American option pricer using the Snell's envelope concept """

        price_tree = [[0.0] * (self.num_intervals + 1)] * (self.num_intervals + 1)
        stopping_tree = [[False] * (self.num_intervals + 1)] * (self.num_intervals + 1)
        m = self.num_intervals - 1  # intermediate steps
        for i in range(self.num_intervals + 1):  # including n
            price_tree[self.num_intervals][i] = self.payoff(binmodel.calculateStockPriceBinominal(self.st, self.num_intervals, i))
            stopping_tree[self.num_intervals][i] = True
        while m >= 0:
            for i in range(m + 1):
                val1 = (binmodel.q * price_tree[m+1][i+1] + (1 - binmodel.q) * price_tree[m+1][i]) \
                       / (1 + binmodel.r)
                val2 = self.payoff(binmodel.calculateStockPriceBinominal(self.st, m, i))
                price_tree[m][i] = val1 if val1 > val2 else val2
                stopping_tree[m][i] = True if val1 > val2 else False
            m -= 1
        return price_tree[0][0]

    def approximateBS(self, bsm):
        """ The approximation of BSM by means of binomial tree """

        # calibrate u,d,r
        u = math.exp((bsm.r+bsm.sigma**2/2)*self.h + bsm.sigma*math.sqrt(self.h)) - 1
        d = math.exp((bsm.r+bsm.sigma**2/2)*self.h - bsm.sigma*math.sqrt(self.h)) - 1
        r = math.exp(bsm.r*self.h) - 1
        binmodel = bn.BinomialModel(u, d, r)

        # kick off CRR pricer
        return self.calculateOptionPriceBySnell(binmodel)


class Call(EurOpt, AmOpt):

    def __init__(self):
        super().__init__()
        self.strike = float(input("Pass strike price (K): "))
        while self.strike < 0:
            print("Strike price also has to be positive number.")
            self.strike = float(input("Pass strike price (K): "))

    def payoff(self, price):
        return aux.maximum(price - self.strike, 0) # max function

    @aux.execution_time
    def calculateOptionPriceBSM(self, bsm):
        d_plus = 1/(bsm.sigma*np.sqrt(self.time_to_maturity))*\
                 (np.log(self.st/self.strike) + (bsm.r + 0.5*bsm.sigma**2)*self.time_to_maturity)
        d_minus = d_plus - bsm.sigma*np.sqrt(self.time_to_maturity)
        return sc.norm.cdf(d_plus)*self.st - sc.norm.cdf(d_minus)*self.strike*np.exp(-bsm.r*self.time_to_maturity)


class Put(EurOpt, AmOpt):

    def __init__(self):
        super().__init__()
        self.strike = float(input("Pass strike price (K): "))
        while self.strike < 0:
            print("Strike price also has to be positive number.")
            self.strike = float(input("Pass strike price (K): "))

    def payoff(self, price):
        return aux.maximum(self.strike - price, 0)

    @aux.execution_time
    def calculateOptionPriceBSM(self, bsm):
        d_plus = 1/(bsm.sigma*np.sqrt(self.time_to_maturity))*\
                 (np.log(self.st/self.strike) + (bsm.r + 0.5*bsm.sigma**2)*self.time_to_maturity)
        d_minus = d_plus - bsm.sigma*np.sqrt(self.time_to_maturity)
        return sc.norm.cdf(-d_minus)*self.strike*np.exp(-bsm.r*self.time_to_maturity) - sc.norm.cdf(-d_plus)*self.st


class DoubleDigit(EurOpt):
    """ double digit option, an example of option with two strike prices"""
    def __init__(self):
        super().__init__()
        self.strike = []
        self.strike.append(float(input("Pass lower strike price (K1): ")))
        self.strike.append(float(input("Pass lower strike price (K2): ")))
        while (self.strike[0] < 0) or (self.strike[1] < 0):
            print("Strike prices have to be greater than zero.")
            # They're already existing
            self.strike[0] = float(input("Pass lower bound (K1): "))
            self.strike[1] = float(input("... and upper one (K2): "))

    def payoff(self, price):
        return 1 if self.strike[0] < price < self.strike[1] else 0