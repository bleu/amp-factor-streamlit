import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.market_makers import LinearInvariant, Uniswap

st.set_page_config(
   page_title="Home | Amp Factor",
   page_icon="🏠",
   initial_sidebar_state="expanded",
)

st.title('Amp Factor Dashboard')

st.write('The goal of this dashboard is to simulate how stable pools would behave with different Amp Factors. It also aims to help the understanding of the impact of the Amp Factor and how Stable Pool works mathematically.')
st.write('If you want to understand more about Stable pools you can continue reading. If you want to use the simulation, feel free to change to the stable curve page on the sidebar.')
st.write('*This dashboard was developed by [luizakp](https://github.com/luizakp) and [yvesfracari](https://github.com/yvesfracari)*')

st.header('Learning more about StablePool')

st.write('First of all, StablePools are the ones that perform StableSwaps, which is an Autonomous Market Maker (AMM) for stablecoins, meaning that **the price adjustment between the tokens is defined by a deterministic algorithm.** If you have the same input you will have the same output.')
st.write('StableSwaps are mathematically the combination between **constant sum formula** and **constant product formula (Uniswap)**')

st.subheader('Constant sum formula')

st.write('Here the constant is equal to the sum of the initial amount of tokens. So **x+y = k**. After a swap, the constant will remain the same, which will define the price and amount of tokens the user will receive in return for selling a certain amount of tokens.')
st.write('You will notice that with this formula the price is always 1, which there is no price impact but the pool can be completely drained.')
st.write('For a better understanding, please use this simulation:')

balance_x_sum = st.number_input('Insert the initial amount of token X', value=2, step=1)
balance_y_sum = st.number_input('Insert the initial amount of token Y', value=2, step=1)
x_data_sum = {'name':'X', 'balance': balance_x_sum}
y_data_sum = {'name':'Y', 'balance': balance_y_sum}
type_of_tokens = ['','X','Y']

linear_invariant = LinearInvariant(x=balance_x_sum, y=balance_y_sum)

st.write('K is equal to ', linear_invariant.constant)

type_token_sell_sum = st.selectbox(label="Which token do you want to sell?", options=type_of_tokens, key="sum")

x_sum = np.linspace(0, linear_invariant.constant)
y_sum = np.linspace(0, linear_invariant.constant)

fig = px.line(x=x_sum, y= linear_invariant.constant-x_sum, title='Line Invariant Pool Chart')

if type_token_sell_sum:
  tokens_data_sum = linear_invariant.define_binary_sell_buy(type_token_sell_sum, x_data_sum, y_data_sum)
  type_token_buy_sum = tokens_data_sum['type_token_buy']
  initial_amount_sell_sum = tokens_data_sum['initial_amount_sell']
  initial_amount_buy_sum = tokens_data_sum['initial_amount_buy']
  amount_token_sell_sum = st.number_input(label='How much of token {} you want to sell?'.format(type_token_sell_sum),value=2.0, step=0.1,max_value=float(initial_amount_buy_sum), min_value=0.0)

  if amount_token_sell_sum != 0 :
    transaction_sum = linear_invariant.calculate_trade(initial_amount_sell_sum, initial_amount_buy_sum, amount_token_sell_sum)
    amount_token_buy_sum = transaction_sum['amount_token_buy']
    st.write('You will receive', amount_token_buy_sum, 'of token', type_token_buy_sum)

    price_sum = transaction_sum['price']
    st.write('You paid 1 Y for', price_sum, 'X')

    if type_token_sell_sum == 'X':
        fig.add_scatter(mode="markers",x=transaction_sum['transaction_sell'],y=transaction_sum['transaction_buy'], text=transaction_sum['label'],name="transaction variation", hovertemplate='<br>'.join([
                '%{text}',
                'X: %{x}',
                'Y: %{y}',
            ]),
        )
    else:
        fig.add_scatter(mode="markers",x=transaction_sum['transaction_buy'],y=transaction_sum['transaction_sell'], text=transaction_sum['label'],name="transaction variation", hovertemplate='<br>'.join([
            '%{text}',
            'X: %{x}',
            'Y: %{y}',
        ]),
      )
  else: st.markdown(f'<p style="color:#C52233;">Please select the amount of token {type_token_sell_sum} you want to sell</p>', unsafe_allow_html=True)
    
st.plotly_chart(fig, use_container_width=True)

st.subheader('Constant product formula')

st.write('Here the constant is equal to the product of the initial amount of tokens. So **x*y = k**. The number of tokens will be determined by the equation.')
st.write('Here with every trade, the price will change, which means price impact will exist but the pool can not be drained by giving liquidity as prices approach infinity.')
st.write('For a better understanding, please use this simulation:')

balance_x_product = st.number_input('Insert the initial amount of token X', value=10, step=1)
balance_y_product = st.number_input('Insert the initial amount of token Y', value=10, step=1)
x_data_product = {'name':'X', 'balance': balance_x_product}
y_data_product = {'name':'Y', 'balance': balance_y_product}

uniswap = Uniswap(x=balance_x_product, y=balance_y_product)

st.write('K is equal to ', uniswap.constant)

type_token_sell_product = st.selectbox(label="Which token do you want to sell?", options=type_of_tokens, key="product")

x_product = np.linspace(1, uniswap.constant,num=uniswap.constant)
y_product = np.linspace(1, uniswap.constant,num=uniswap.constant)

fig = px.line(x=x_product, y=(uniswap.constant/x_product), title='Constant product formula Pool Chart')

if type_token_sell_product:
  tokens_data_product = uniswap.define_binary_sell_buy(type_token_sell_product,x_data_product, y_data_product)
  type_token_buy_product = tokens_data_product['type_token_buy']
  initial_amount_sell_product = tokens_data_product['initial_amount_sell']
  initial_amount_buy_product = tokens_data_product['initial_amount_buy']
  amount_token_sell_product = st.number_input(label='How much of token {} you want to sell?'.format(type_token_sell_product),value=2.0, step=0.1,max_value=float(uniswap.constant), min_value=0.1)

  transaction_product = uniswap.calculate_trade(initial_amount_sell_product, initial_amount_buy_product, amount_token_sell_product)
  amount_token_buy_product = transaction_product['amount_token_buy']
  st.write('You will receive', amount_token_buy_product, 'of token', type_token_buy_product)

  price = transaction_product['price']

  if type_token_sell_product == "X":
    st.write('You paid 1 Y for', price, 'X')
    fig.add_scatter(mode="markers",x=transaction_product['transaction_sell'],y=transaction_product['transaction_buy'], text=transaction_product['label'],name="Transaction variation", hovertemplate='<br>'.join([
      '%{text}',
      'X: %{x}',
      'Y: %{y}',
    ]))
  else:
    st.write('You paid 1 X for', price, 'Y')

    fig.add_scatter(mode="markers",x=transaction_product['transaction_buy'],y=transaction_product['transaction_sell'], text=transaction_product['label'],name="Transaction variation", hovertemplate='<br>'.join([
        '%{text}',
        'X: %{x}',
        'Y: %{y}',
    ]))

st.plotly_chart(fig, use_container_width=True)