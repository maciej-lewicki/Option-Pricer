# Binomial model


class BinomialModel:
    """ Basic binomial tree option pricing model
    u/d - move up/down factor, u=1/d (as per Cox-Rubinstein-Ross approach)
    r - simple interest rate """
    def __init__(self, u=False, d=False, r=False):
        # Input data safeguards
        # 0 < S0, -1 < D < U, -1 < R
        if not (u and d and r):
            # Arbitrage collar
            # D < R < U
            self.d = self.r = self.u = 1  # to start the 'arbitrage' loop below
            while (self.d >= self.r) or (self.r >= self.u):
                print("Remember about arbitrage constraints: D < R < U.")
                self.u = float(input("Pass moving up factor (U): "))
                self.d = float(input("Pass moving down factor (D): "))
                while (self.d > self.u) or (self.d <= -1):
                    print(f"U should be greater than D and both should be greater than -1. Try again!")
                    self.u = float(input("U: "))
                    self.d = float(input("D: "))

                self.r = float(input("Pass risk-free rate (the simple one): "))
                while self.r < -1:
                    self.r = float(input("Risk-free rate parameter R should be greater than -1. Try again: "))
        else:
            self.u = u
            self.d = d
            self.r = r
        self.q = (self.r - self.d) / (self.u - self.d)

    def calculateStockPriceBinominal(self, s0, n, i):
        """ returns stock price on i-th node at n-th step, both are integers """
        return s0 * pow(1 + self.u, i) * pow(1 + self.d, n - i)