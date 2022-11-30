import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.market_makers import Uniswap

st.title('Constant product formula')

balanceX = st.number_input('Insert the initial amount of token X', value=10, step=1)
balanceY = st.number_input('Insert the initial amount of token Y', value=10, step=1)

uniswap = Uniswap(x=balanceX, y=balanceY)

k = uniswap.get_constant(balanceX,balanceY)

st.write('K is equal to ', k)

typeTokenSell = st.selectbox(label="Which token you want to sell?", options=['','X','Y'])

x = np.linspace(0, k,num=k)
y = np.linspace(0, k,num=k)

fig = px.line(x=x, y=(k/x), title='Constant product formula Pool Chart')

if typeTokenSell:
  tokensData = uniswap.define_sell_buy(typeTokenSell,balanceX,balanceY)
  typeTokenBuy = tokensData['typeTokenBuy']
  initialAmountSell = tokensData['initialAmountSell']
  initialAmountBuy = tokensData['initialAmountBuy']
  amountTokenSell = st.number_input(label='How much of token {} you want to sell?'.format(typeTokenSell),value=2.0, step=0.1,max_value=float(k), min_value=0.1)

  transaction = uniswap.calculate_trade(initialAmountSell, initialAmountBuy, amountTokenSell)
  amountTokenBuy = transaction['amountTokenBuy']
  st.write('You will receive', amountTokenBuy, 'of token', typeTokenBuy)

  price = transaction['price']

  if typeTokenSell == "X":
    st.write('You paid 1 Y for', price, 'X')
    fig.add_scatter(mode="markers",x=transaction['transactionSell'],y=transaction['transactionBuy'], text=transaction['label'],name="Transaction variation", hovertemplate='<br>'.join([
      '%{text}',
      'X: %{x}',
      'Y: %{y}',
    ]))
  if typeTokenSell == "Y":
    st.write('You paid 1 X for', price, 'Y')

    fig.add_scatter(mode="markers",x=transaction['transactionBuy'],y=transaction['transactionSell'], text=transaction['label'],name="Transaction variation", hovertemplate='<br>'.join([
        '%{text}',
        'X: %{x}',
        'Y: %{y}',
    ]))

st.plotly_chart(fig, use_container_width=True)