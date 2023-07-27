"""
The Black-Scholes model makes certain assumptions:

No dividends are paid out during the life of the option.
Markets are random (i.e., market movements cannot be predicted).
There are no transaction costs in buying the option.
The risk-free rate and volatility of the underlying asset are known and constant.
The returns of the underlying asset are normally distributed.
The option is European and can only be exercised at expiration.

The Black-Scholes call option formula is calculated by multiplying the stock price by the cumulative standard normal
probability distribution function. Thereafter, the net present value (NPV) of the strike price multiplied by the
cumulative standard normal distribution is subtracted from the resulting value of the previous calculation.

Based off of:
https://investopedia.com/terms/b/blackscholes.asp#:~:text=The%20Black-Scholes%20model%2C%20aka,free%20rate%2C%20and%20the%20volatility.

"""
from math import log, sqrt, pi, exp, e
from scipy.stats import norm
from datetime import datetime, date
import numpy as np
import pandas as pd
from pandas import DataFrame


class BlackScholesPricing():

    def __init__(self, volatility, spotprice, strike, timetoMaturity, riskFreeRate):
        self.V = volatility
        self.S = spotprice
        self.str = strike
        self.T = timetoMaturity
        self.R = riskFreeRate

    # sigma is standard dev of log returns or = volatility
    def d1(self):
        return np.log(self.S / self.str) + ((self.R + (np.square(self.V) / 2)) * self.T) / (self.V * np.sqrt(self.T))

    def d2(self):
        return self.d1() - (self.V * self.T)

    def callPrice(self):
        return (self.S * norm.cdf(self.d1())) - (self.str * (e ** (-self.R * self.T) * norm.cdf(self.d2())))

    def putPrice(self):
        return (self.S * e ** (-self.R * self.T)) - self.str + self.callPrice()


bs1 = BlackScholesPricing(0.2, 25, 15, 3.5, 0.05)
print(bs1.callPrice())
print(bs1.putPrice())
