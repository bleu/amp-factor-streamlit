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

  @abstractmethod
  def define_sell_buy(self):
    pass

  @abstractmethod
  def calculate_trade(self):
    pass

class LinearInvariant(MarketMaker):
  def get_constant(self, x, y):
    return x+y
  
  def calculate_y(self, x):
    return self.constant - x
  
  def calculate_spot_price(self):
    return 1

  def define_sell_buy(self, type_token_sell, balance_x, balance_y):
    if type_token_sell == 'X':
      tokensData = {
        'type_token_buy': 'Y',
        'initial_amount_sell': balance_x,
        'initial_amount_buy': balance_y,
      }
      return tokensData
    else:
      tokensData = {
        'type_token_buy': 'X',
        'initial_amount_sell': balance_y,
        'initial_amount_buy': balance_x,
      }
      return tokensData

  def calculate_trade(self, initial_amount_sell, initial_amount_buy, amount_token_sell):
    amount_token_buy = initial_amount_sell + initial_amount_buy + amount_token_sell - self.constant
    price = amount_token_buy/amount_token_sell
    final_amount_sell = initial_amount_sell+amount_token_sell
    final_amount_buy = initial_amount_buy-amount_token_buy

    transaction = {
      'amount_token_buy': amount_token_buy,
      'price': price,
      'transaction_sell': [initial_amount_sell,final_amount_sell],
      'transaction_buy': [initial_amount_buy,final_amount_buy],
      'label': ['Before the trade', 'After the trade']
    }

    return transaction


class Uniswap(MarketMaker):
  def get_constant(self, x, y):
    return x*y
  
  def calculate_y(self, x):
    return self.constant / x
  
  def calculate_spot_price(self, x):
    return self.constant / (x**2)

  def define_sell_buy(self, type_token_sell, balance_x, balance_y):
    if type_token_sell == 'X':
      tokensData = {
        'type_token_buy': 'Y',
        'initial_amount_sell': balance_x,
        'initial_amount_buy': balance_y,
      }
      return tokensData
    else:
      tokensData = {
        'type_token_buy': 'X',
        'initial_amount_sell': balance_y,
        'initial_amount_buy': balance_x,
      }
      return tokensData

  def calculate_trade(self, initial_amount_sell, initial_amount_buy, amount_token_sell):
    amount_token_buy = (initial_amount_buy * amount_token_sell) / (initial_amount_sell+amount_token_sell)
    price = amount_token_buy/amount_token_sell
    final_amount_sell = initial_amount_sell+amount_token_sell
    final_amount_buy = initial_amount_buy-amount_token_buy

    transaction = {
      'amount_token_buy': amount_token_buy,
      'price': price,
      'transaction_sell': [initial_amount_sell,final_amount_sell],
      'transaction_buy': [initial_amount_buy,final_amount_buy],
      'label': ['Before the trade', 'After the trade']
    }

    return transaction

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
    first_part = self.amp * self.constant + ((self.constant/2)**2) - self.amp*x
    second_part = 1/(self.amp+x)
    return first_part * second_part

  def calculate_spot_price(self, x):
    part1 = 1/(self.amp+x)
    part21 = self.amp
    part221 = (self.amp*self.constant)+((self.constant**2)*0.25)-(self.amp*x)
    part222 = 1/(self.amp+x)
    return part1*(part21+(part221*part222))

  def calculate_trade(): 
    pass
  
  def define_sell_buy():
    pass