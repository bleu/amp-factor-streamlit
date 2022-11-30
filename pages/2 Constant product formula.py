import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.market_makers import Uniswap

st.title('Constant product formula')

balance_x = st.number_input('Insert the initial amount of token X', value=10, step=1)
balance_y = st.number_input('Insert the initial amount of token Y', value=10, step=1)

uniswap = Uniswap(x=balance_x, y=balance_y)

st.write('uniswap.constant is equal to ', uniswap.constant)

type_token_sell = st.selectbox(label="Which token you want to sell?", options=['','X','Y'])

x = np.linspace(0, uniswap.constant,num=uniswap.constant)
y = np.linspace(0, uniswap.constant,num=uniswap.constant)

fig = px.line(x=x, y=(uniswap.constant/x), title='Constant product formula Pool Chart')

if type_token_sell:
  tokens_data = uniswap.define_sell_buy(type_token_sell,balance_x,balance_y)
  type_token_buy = tokens_data['type_token_buy']
  initial_amount_sell = tokens_data['initial_amount_sell']
  initial_amount_buy = tokens_data['initial_amount_buy']
  amount_token_sell = st.number_input(label='How much of token {} you want to sell?'.format(type_token_sell),value=2.0, step=0.1,max_value=float(uniswap.constant), min_value=0.1)

  transaction = uniswap.calculate_trade(initial_amount_sell, initial_amount_buy, amount_token_sell)
  amount_token_buy = transaction['amount_token_buy']
  st.write('You will receive', amount_token_buy, 'of token', type_token_buy)

  price = transaction['price']

  if type_token_sell == "X":
    st.write('You paid 1 Y for', price, 'X')
    fig.add_scatter(mode="markers",x=transaction['transaction_sell'],y=transaction['transaction_buy'], text=transaction['label'],name="Transaction variation", hovertemplate='<br>'.join([
      '%{text}',
      'X: %{x}',
      'Y: %{y}',
    ]))
  else:
    st.write('You paid 1 X for', price, 'Y')

    fig.add_scatter(mode="markers",x=transaction['transaction_buy'],y=transaction['transaction_sell'], text=transaction['label'],name="Transaction variation", hovertemplate='<br>'.join([
        '%{text}',
        'X: %{x}',
        'Y: %{y}',
    ]))

st.plotly_chart(fig, use_container_width=True)