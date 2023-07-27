"""
Basic Algorithm:
1.Build a binary tree
2.Take the current price (spot price) of the stock  S
3.create a condition for an upward and downward price movement u and d in which
  uS = S+ (or the stock price increases) and ud = S- (stock price decreases)
  d can often times be simply 1/u or something simple, depends on the complexity of the model

For options (puts or calls) they entitle the holder to buy the underlying stock at exercise price Px
a call option is ITM (in-the-money) when S > Px
4.To calculate the payoff of a call option: you simply take the maximum between 0 and (uS - Px) or (dS - Px)
    so C+ = max(0, S+) and C- = max(0, S-)
    or
4.To calculate the payoff of a put option: you simply take the maximum between (Px - uS) or (Px - dS) and 0
    so P+ = max(S+, 0) and P- = max(P-, 0)
5.Then the binomial model weights the different payoffs with their respective probabilities and then discounts to PV

6.To arrive at the present value of a call option: c = (pi(C+) + (1-pi)(C-))/(1 + r) where pi is the probability of an
  up move and r is the discount rate

  pi = ((1 + tr) - d)/(u - d) where: t is the period multiplier (so 6mo -> 0.5), r is the discount rate, and u and d are
  up and down factors

7.So each node is option price after each period where the first option is C, then each subsequent child node is C+
resources:
https://www.codearmo.com/python-tutorial/options-trading-binomial-pricing-model
https://github.com/krivi95/option-pricing-models/blob/master/option_pricing/BinomialTreeModel.py
https://www.macroption.com/binomial-option-pricing-model-inputs/
https://www.wallstreetmojo.com/binomial-option-pricing-model/#h-what-is-binomial-option-pricing-model
https://magnimetrics.com/understanding-the-binomial-option-pricing-model/
"""
import numpy as np
import math
import matplotlib


# creating Binary tree to store values
# edit: not needed
class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def PrintTree(self):
        print(self.data)

    def insert(self, data):
        # Compare the new value with the parent node
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.left)
            res.append(root.data)
            res = res + self.inorderTraversal(root.right)
        return res


# Pricing Model
class BinomialPricingModel:
    # period_len should be in days
    def __init__(self, spot_price, rfr, period_len, strike, otype, vol, numtimesteps):
        self.S = spot_price
        self.R = rfr
        self.T = period_len / 365
        # vol would be the volatility of the underlying asset
        self.V = vol
        self.otype = otype
        self.strike = strike
        self.numtimesteps = numtimesteps

    def calloptionprice(self):
        # calculating up & down factors and delT
        delT = self.T / self.numtimesteps
        # calculation for U factor taken from random internet source
        u = np.exp(self.V * np.sqrt(delT))
        d = 1.0 / u

        # calculating the probabilities of an up or down movement
        p = (1 + (self.T * self.R) - d) / (u - d)
        q = 1 - p

        # calculating the stock price should be either u * S or d * S and then placed at the level after node (S)
        # calculating option price for each of these levels has to occur starting from the back
        # initialize stock price vector
        pvector = np.zeros(self.numtimesteps + 1)

        # calculate a stock price tree (underlying asset price calculation), and store in numpy array
        S_t = np.array([(self.S * u ** j * d ** (self.numtimesteps - j)) for j in range(self.numtimesteps + 1)])

        a = np.exp(self.R * delT)  # rf compunded return
        # p = (a - d) / (u - d)  # rf neutral up probability
        # q = 1.0 - p

        pvector[:] = np.maximum(S_t - self.strike, 0.0)

        # returning new option prices in price vector
        for i in range(self.numtimesteps - 1, -1, -1):
            pvector[:-1] = np.exp(-self.R * delT) * (p * pvector[1:] + q * pvector[:-1])

        return pvector[0]

    def putoptionprice(self):
        # calculating up & down factors and delT
        delT = self.T / self.numtimesteps
        # calculation for U factor taken from random internet source
        u = np.exp(self.V * np.sqrt(delT))
        d = 1.0 / u

        # calculating the probabilities of an up or down movement
        p = (1 + (self.T * self.R) - d) / (u - d)
        q = 1 - p

        # calculating the stock price should be either u * S or d * S and then placed at the level after node (S)
        # calculating option price for each of these levels has to occur starting from the back
        # initialize stock price vector
        pvector = np.zeros(self.numtimesteps + 1)

        # calculate a stock price tree (underlying asset price calculation), and store in numpy array
        S_t = np.array([(self.S * u ** j * d ** (self.numtimesteps - j)) for j in range(self.numtimesteps + 1)])

        a = np.exp(self.R * delT)  # rf compunded return
        pvector[:] = np.max(self.strike - S_t, 0)

        # returning new option prices in price vector
        for i in range(self.numtimesteps - 1, -1, -1):
            pvector[:-1] = np.exp(-self.R * delT) * (p * pvector[1:] + q * pvector[:-1])

        return pvector[0]
