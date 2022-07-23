# Options container class

from abc import ABC, abstractmethod
import math
import auxiliary as aux
import Binomial as bn


class Options(ABC):
    """ Options class container
    we apply ABC class/module to create abstract methods """
    def __init__(self):
        self.time_to_maturity = int(input("Pass time to expiration (in years): "))
        self.N = int(input("Pass number of intervals: "))
        while self.N < 0 or self.time_to_maturity < 0:
            print("Number of intervals (N) should be higher than 0, the same for time to maturity (T)")
            self.time_to_maturity = int(input("Pass time to maturity: "))
            self.N = int(input("Pass number of intervals: "))
        self.h = float(self.time_to_maturity / self.N)

        self.s0 = float(input("Pass initial underlying price: "))
        while self.s0 < 0:
            self.s0 = float(input("S0 should be non-negative number. Try again: "))

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
            m = self.N - 1  # intermediate steps
            price = []
            for i in range(self.N + 1):  # including n
                price.append(self.payoff(binmodel.calculateStockPriceBinominal(self.s0, self.N, i)))
            while m >= 0:
                for i in range(m+1):
                    price[i] = (binmodel.q*price[i+1]+(1-binmodel.q)*price[i])/(1+binmodel.r)
                m -= 1
            final_price = price[0]
        elif method == 'aggregated':
            final_price = math.factorial(self.N) / pow((1 + binmodel.r), self.N) \
                          * sum((1 / (math.factorial(i) * math.factorial(self.N - i)) * pow(binmodel.q, i)
                                 * pow(1 - binmodel.q, self.N - i)
                                 * self.payoff(binmodel.calculateStockPriceBinominal(self.s0, self.N, i))
                                 for i in range(self.N + 1)))  # including n, generator is enough
            # TODO: check the alternative solution with condition checking embedded in the index (Hull, p. 298)
        else:
            print('Wrong method name - try again with iterative or aggregated')
        return final_price


class AmOpt(Options):
    """ American Options """

    @aux.execution_time
    def calculateOptionPriceBySnell(self, binmodel):
        """ American option pricer using the Snell's envelope concept """

        price_tree = [[0.0] * (self.N + 1)] * (self.N + 1)
        stopping_tree = [[False] * (self.N + 1)] * (self.N + 1)
        m = self.N - 1  # intermediate steps
        for i in range(self.N + 1):  # including n
            price_tree[self.N][i] = self.payoff(binmodel.calculateStockPriceBinominal(self.s0, self.N, i))
            stopping_tree[self.N][i] = True
        while m >= 0:
            for i in range(m + 1):
                val1 = (binmodel.q * price_tree[m+1][i+1] + (1 - binmodel.q) * price_tree[m+1][i]) \
                       / (1 + binmodel.r)
                val2 = self.payoff(binmodel.calculateStockPriceBinominal(self.s0, m, i))
                price_tree[m][i] = val1 if val1 > val2 else val2
                stopping_tree[m][i] = True if val1 > val2 else False
            m -= 1
        return price_tree[0][0]

    def approximateBlackScholes(self, bsm):
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


class Put(EurOpt, AmOpt):

    def __init__(self):
        super().__init__()
        self.strike = float(input("Pass strike price (K): "))
        while self.strike < 0:
            print("Strike price also has to be positive number.")
            self.strike = float(input("Pass strike price (K): "))

    def payoff(self, price):
        return aux.maximum(self.strike - price, 0)


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