"""
http://www.goddardconsulting.ca/option-pricing-monte-carlo-index.html
https://onlinelibrary.wiley.com/doi/full/10.1002/fut.21647?casa_token=iFNqcqNeEKYAAAAA%3AX5_prQchKTufEdF0eNrnMQ-GT-TXI4gH7oMoi_wJpgG321mJM18PB7JHJwKtvMkeHmuuOlhQ4q8cif0
https://fincad.com/resources/resource-library/article/monte-carlo-simulation-derivatives-valuation#:~:text=Today%2C%20Monte%20Carlo%20methods%20are,notions%20and%20measures%20of%20risk.

"""

import numpy as np
import matplotlib.pyplot as plt


class MonteCarloSim():

    def __init__(self, stock_price, strike_price, ttm, risk_free_rate, div_yield, vol, steps, N):
        self.S = stock_price
        self.k = strike_price
        self.t = ttm
        self.r = risk_free_rate
        self.q = div_yield
        self.sigma = vol
        self.st = steps
        self.N = N

    def geo_paths(self):
        # [steps,N] Matrix of asset paths
        dt = self.t / self.st
        # S_{T} = ln(S_{0})+\int_{0}^T(\mu-\frac{\sigma^2}{2})dt+\int_{0}^T \sigma dW(t)
        ST = np.log(self.S) + np.cumsum(((self.r - self.q - self.sigma ** 2 / 2) * dt +
                                         self.sigma * np.sqrt(dt) * np.random.normal(size=(self.st, self.N))), axis=0)
        return np.exp(ST)


"""
S = 100  # stock price S_{0}
K = 110  # strike
T = 1 / 2  # time to maturity
r = 0.05  # risk-free risk in annual %
q = 0.02  # annual dividend rate
sigma = 0.25  # annual volatility in %
steps = 100  # time steps
N = 1000  # number of trials
"""

mcs1 = MonteCarloSim(100, 110, 1 / 2, 0.05, 0.02, 0.25, 100, 1000)
paths = mcs1.geo_paths()

plt.plot(paths)
plt.xlabel("Time Increments")
plt.ylabel("Stock Price")
plt.title("Geometric Brownian Motion")
