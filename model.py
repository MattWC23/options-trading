from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self, size=0):
        self.options = [] * size


    @abstractmethod
    def call_and_put_price(self, option):
        """
        Returns call and put price for an option (call, put)
        """
        pass
    
    @abstractmethod
    def add_option(self, option):
        """
        Adds the option to the model to be stored for its call and put price
        and returns (call, put)
        """
        pass

    @abstractmethod
    def all_prices(self, option):
        """
        Returns all call, put pairs for all options in the model
        """
    
    def __str__(self):
        output = []
        for option in self.options:
            name, (call, put) = next(iter(option.items()))
            output.append(f'{name}: Call(${call}, Put(${put}))')
        
        return str(output)
    


class Option():

    def __init__(self, S, K, T, r, sigma, name):
        """
        Create an option with Underlying Price, 'S', Strike Price 'K',
        Time to Expiration, 'T', Risk Free Rate, 'r', and Volatility, 'sigma'
        """
        self.name = name
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
    
