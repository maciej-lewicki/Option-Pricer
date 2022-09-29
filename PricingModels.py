# Pricing models

import numpy as np
import scipy.stats as sc

class BlackScholes:
    """ Infamous Black-Scholes (-Merton) model
    It's a stub so far, will be developed in next iterations """

    def __init__(self, st=False, mu=False, sigma=False, r=False):
        # Input data safeguards
        # 0 < S0, sigma > 0, R, mu - unbounded
        # Variance = sigma**2
        # if not st:
        #     self.st = float(input("Pass stock price: "))
        #     while self.st < 0:
        #         self.st = float(input("St should be non-negative number. Try again: "))
        # else:
        #     self.st = st
        if not (mu and sigma and r):
            self.mu = self.r = self.sigma = -1  # to start the 'arbitrage' loop below
            self.mu = float(input("Pass a drift parameter (mu): "))
            while self.sigma < 0:
                self.sigma = float(input("Pass a volatility parameter (sigma). It should be greater than 0: "))
                if self.sigma < 0:
                    print("Try again!")
            self.r = float(input("Pass risk-free rate (continuously compounded): "))
        else:
            self.mu = mu
            self.sigma = sigma
            self.r = r

    def generateSamplePath(self, st, grid, dfs):
        """ Using the analytical solution of geometric Brownian motion """
        # the grid is equally-distant at the moment
        n = len(grid)
        s_tk = np.zeros(n)
        s_tk[0] = st
        z = sc.norm.rvs(size=n-1)
        for num, zk in enumerate(z, 1):
            s_tk[num] = s_tk[num-1] * np.exp(self.sigma*np.sqrt(grid[num] - grid[num-1])*zk) * dfs[num]
        return s_tk
