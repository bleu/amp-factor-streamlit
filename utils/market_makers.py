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
  
  @abstractmethod
  def calculate_spot_price(self):
    pass


class LinearInvariant(MarketMaker):
  def get_constant(self, x, y):
    return x+y
  
  def calculate_y(self, x):
    return self.constant - x
  
  def calculate_spot_price(self):
    return 1


class Uniswap(MarketMaker):
  def get_constant(self, x, y):
    return x+y
  
  def calculate_y(self, x):
    return self.constant / x
  
  def calculate_spot_price(self, x):
    return self.constant / (x**2)

class StableSwapBinary(MarketMaker):
  def __init__(self, **kwargs):
    self.amp = kwargs["amp"]
    super().__init__(**kwargs)

  def get_constant(self, x, y, amp):
      a = 1/4
      b = amp
      c = -1 * ((amp * (x+y)) + (x*y))
      delta = ((b**2) - (4*a*c))**(1/2) 
      return (-b + delta)/(2*a)

  def calculate_y(self, x):
    first_part = self.amp * self.constant + ((self.constant**2)/4) - self.amp*x
    second_part = (self.amp+x)**(-1)
    return first_part * second_part

  def calculate_spot_price(self, x):
    part1 = 1/(self.amp+x)
    part21 = self.amp
    part221 = (self.amp*self.constant)+((self.constant**2)*0.25)-(self.amp*x)
    part222 = 1/(self.amp+x)
    return part1*(part21+(part221*part222))
