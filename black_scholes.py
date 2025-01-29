from model import Model, Option
import math
from scipy.stats import norm

class BlackScholes(Model):

    def __init__(self, size=0):
        super().__init__(size)
    
    def call_and_put_price(self, option): 
        d1, d2 = self._calc_d1_and_d2(option)
        call = self._calc_call_option(option, d1, d2)
        put = self._calc_put_option(option, d1, d2)
        return (call, put)
    
    def add_option(self, option):
        val = self.call_and_put_price(option)
        self.options.append({option.name, val})
        return val

    def _calc_d1_and_d2(self, option):
        S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        return d1, d2
    
    def _calc_call_option(self, option, d1, d2):
        return option.S * norm.cdf(d1) - option.K * math.exp(-option.r * option.T) * norm.cdf(d2)
    
    def _calc_put_option(self, option, d1, d2):
        return option.K * math.exp(-option.r * option.T) * norm.cdf(-d2) - option.S * norm.cdf(-d1)
    

    def all_prices(self, option):
        return super().all_prices(option)
    

