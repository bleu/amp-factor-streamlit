from abc import ABC, abstractmethod, abstractproperty


class MarketMaker(ABC):
  def __init__(self, **kwargs):
    self.constant = self.get_constant(**kwargs)
  
  @abstractmethod
  def get_constant(self):
    pass

  @abstractmethod
  def calculate_y(self):
    pass


class LinearInvariant(MarketMaker):
  def get_constant(self, x, y):
    return x+y
  
  def calculate_y(self, x):
    return self.constant - x


class Uniswap(MarketMaker):
  def get_constant(self, x, y):
    return x+y
  
  def calculate_y(self, x):
    return self.constant / x

class StableSwap(MarketMaker):
  def get_constant(self, x, y, amp):
      a = 1/4
      b = amp
      c = -1 * ((amp * (x+y)) + (x*y))
      delta = ((b**2) - (4*a*c))**(1/2) 
      return (-b + delta)/(2*a)

  def calculate_y(self, x, amp):
    first_part = amp * self.constant + ((self.constant**2)/4) - amp*x
    second_part = (amp+x)**(-1)
    return first_part * second_part