from abc import ABC, abstractmethod
import math
from model import Model


class BinomialModel(Model):
    def __init__(self, size=0, steps=100):
        """
        Initialize the binomial model with a specified number of steps.
        """
        super().__init__(size)
        self.steps = steps

    def call_and_put_price(self, option):
        """
        Calculate the call and put prices using the binomial tree method.
        """
        call, put = self._binomial_pricing(option)
        return (call, put)

    def add_option(self, option):
        """
        Add the option to the model and calculate its prices.
        """
        val = self.call_and_put_price(option)
        self.options.append({option.name: val})
        return val

    def _binomial_pricing(self, option):
        """
        Perform the binomial option pricing calculation.
        """
        S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
        dt = T / self.steps  # Time per step
        u = math.exp(sigma * math.sqrt(dt))  # Up factor
        d = 1 / u  # Down factor
        p = (math.exp(r * dt) - d) / (u - d)  # Risk-neutral probability

        # Create the binomial tree
        prices = [0] * (self.steps + 1)
        for i in range(self.steps + 1):
            prices[i] = S * (u ** i) * (d ** (self.steps - i))

        # Calculate option values at maturity
        call_values = [max(0, price - K) for price in prices]
        put_values = [max(0, K - price) for price in prices]

        # Backward induction through the tree
        for step in range(self.steps - 1, -1, -1):
            for i in range(step + 1):
                call_values[i] = math.exp(-r * dt) * (p * call_values[i + 1] + (1 - p) * call_values[i])
                put_values[i] = math.exp(-r * dt) * (p * put_values[i + 1] + (1 - p) * put_values[i])

        return call_values[0], put_values[0]