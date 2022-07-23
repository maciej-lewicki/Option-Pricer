# Infamous Black-Scholes (-Merton) model

class BLackScholes:
    """ Black Scholes model cass
    It's a stub so far, will be developed in next iterations """

    def __init__(self, s0=False, mu=False, sigma=False, r=False):
        # Input data safeguards
        # 0 < S0, sigma > 0, R, mu - unbounded
        # Variance = sigma**2
        if not s0:
            self.s0 = float(input("Pass initial stock price: "))
            while self.s0 < 0:
                self.s0 = float(input("S0 should be non-negative number. Try again: "))
        else:
            self.s0 = s0
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

