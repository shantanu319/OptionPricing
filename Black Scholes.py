"""
Sources:
https://economictimes.indiatimes.com/definition/black-scholes-model
https://www.albany.edu/~bd445/Economics_802_Financial_Economics_Slides_Fall_2013/Black-Scholes_Option_Pricing.pdf
https://www.cs.princeton.edu/courses/archive/fall09/cos323/papers/black_scholes73.pdf
https://medium.com/swlh/calculating-option-premiums-using-the-black-scholes-model-in-python-e9ed227afbee
https://medium.datadriveninvestor.com/black-scholes-and-option-greeks-in-python-6038f184801e
https://cklixx.people.wm.edu/teaching/math400/Chen-paper2.pdf
http://www.math.uchicago.edu/~may/VIGRE/VIGRE2010/REUPapers/Turner.pdf
Pitfalls:
https://www.investopedia.com/articles/active-trading/041015/how-circumvent-limitations-blackscholes-model.asp

"""
import math
import numpy as np
from scipy.stats import lognorm


class BlackScholesPricing:

    def __init__(self, stock_price, strike_price, risk_free_rate, ttexpiration, ivol):
        self.S = stock_price
        self.K = strike_price
        self.R = risk_free_rate
        self.T = ttexpiration / 365  # to be expressed in years
        self.sigma = ivol

    # lognormal distribution function (x must be > 0)
    def N(self, x):
        if x < 0:
            return 0
        else:
            return 1 - math.exp(-x ** 2 / 2) / math.sqrt(2 * math.pi)

    # for european options
    def euroCallPrice(self):
        t = self.T
        k = self.K
        s = self.S
        r = self.R
        sig = self.sigma

        d1 = ((math.log(s / k, math.e)) + (r + ((pow(sig, 2)) / 2) * t)) / (sig * (math.sqrt(t)))
        d2 = d1 - (sig * math.sqrt(t))

        Nd1 = self.N(d1)
        Nd2 = self.N(d2)

        # 0.728 and 0.584 are test values of Nd1 and Nd2 from a paper provided by Ruo Chen
        return (Nd1 * s) - (Nd2 * k * pow(math.e, -1 * r * t))

    # based on put-call parity
    def euroPutPrice(self):
        callPrice = self.euroCallPrice()
        return callPrice + (self.K / (math.pow(1 + self.R, self.T))) - self.S

    # Merton's extension for stocks with dividends (dividend yield %)
    def McallPrice(self, q):
        t = self.T
        k = self.K
        s = self.S * (math.e ** (-1 * q * t)) #difference maker
        r = self.R
        sig = self.sigma

        d1 = ((math.log(s / k, math.e)) + (r + ((pow(sig, 2)) / 2) * t)) / (sig * (math.sqrt(t)))
        d2 = d1 - (sig * math.sqrt(t))

        Nd1 = self.N(d1)
        Nd2 = self.N(d2)

        return (Nd1 * s) - (Nd2* k * pow(math.e, -1 * r * t))

    def MputPrice(self, q):
        t = self.T
        k = self.K
        s = self.S * (math.e ** (-1 * q * t))  # difference maker
        r = self.R
        sig = self.sigma

        d1 = ((math.log(s / k, math.e)) + (r + ((pow(sig, 2)) / 2) * t)) / (sig * (math.sqrt(t)))
        d2 = d1 - (sig * math.sqrt(t))

        # also a difference in the merton derivation
        Nd1 = self.N(-1 * d1)
        Nd2 = self.N(- 1 * d2)

        return (Nd2 * k * pow(math.e, -1 * r * t)) - (Nd1 * s)


"""c1 = BlackScholesPricing(117.25, 100, 0.085, 92, 0.8445)
print(c1.euroCallPrice())
print(c1.euroPutPrice())
"""

"""
Cox-Ross-Rubenstein for pricing American Options
https://xilinx.github.io/Vitis_Libraries/quantitative_finance/2019.2/methods/bt-crr.html
"""

class Greeks():

    def __init__(self):



    def delta(self):


    def gamma(self):


    def vega(self):


    def theta(self):

    def Rho(self):





