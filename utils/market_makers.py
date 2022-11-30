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
  def define_sell_buy(self):
    pass

  @abstractmethod
  def calculate_trade(self):
    pass

class LinearInvariantBinary(MarketMaker):
  def get_constant(self, x, y):
    return x+y
  
  def calculate_y(self, x):
    return self.constant - x

  def define_sell_buy(self,typeTokenSell,balanceX,balanceY):
    if typeTokenSell == 'X':
      tokensData = {
        'typeTokenBuy': 'Y',
        'initialAmountSell': balanceX,
        'initialAmountBuy': balanceY,
      }
      return tokensData
    if typeTokenSell == 'Y': 
      tokensData = {
        'typeTokenBuy': 'X',
        'initialAmountSell': balanceY,
        'initialAmountBuy': balanceX,
      }
      return tokensData

  def calculate_trade(self, initialAmountSell, initialAmountBuy, amountTokenSell):
    k =  initialAmountSell + initialAmountBuy
    amountTokenBuy = initialAmountSell + initialAmountBuy + amountTokenSell - k
    price = amountTokenBuy/amountTokenSell
    finalAmountSell = initialAmountSell+amountTokenSell
    finalAmountBuy = initialAmountBuy-amountTokenBuy

    transaction = {
      'amountTokenBuy': amountTokenBuy,
      'price': price,
      'transactionSell': [initialAmountSell,finalAmountSell],
      'transactionBuy': [initialAmountBuy,finalAmountBuy],
      'label': ['Before the trade', 'After the trade']
    }

    return transaction


class Uniswap(MarketMaker):
  def get_constant(self, x, y):
    return x*y
  
  def calculate_y(self, x):
    return self.constant / x

  def define_sell_buy(self,typeTokenSell,balanceX,balanceY):
    if typeTokenSell == 'X':
      tokensData = {
        'typeTokenBuy': 'Y',
        'initialAmountSell': balanceX,
        'initialAmountBuy': balanceY,
      }
      return tokensData
    if typeTokenSell == 'Y': 
      tokensData = {
        'typeTokenBuy': 'X',
        'initialAmountSell': balanceY,
        'initialAmountBuy': balanceX,
      }
      return tokensData
  
  def calculate_trade(self, initialAmountSell, initialAmountBuy, amountTokenSell):
    amountTokenBuy = (initialAmountBuy * amountTokenSell) / (initialAmountSell+amountTokenSell)
    price = amountTokenBuy/amountTokenSell
    finalAmountSell = initialAmountSell+amountTokenSell
    finalAmountBuy = initialAmountBuy-amountTokenBuy

    transaction = {
      'amountTokenBuy': amountTokenBuy,
      'price': price,
      'transactionSell': [initialAmountSell,finalAmountSell],
      'transactionBuy': [initialAmountBuy,finalAmountBuy],
      'label': ['Before the trade', 'After the trade']
    }

    return transaction

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

  def calculate_trade():
    pass
  
  def define_sell_buy():
    pass