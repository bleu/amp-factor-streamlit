import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.market_makers import LinearInvariant

st.title('Amp Factor Dashboard')

st.write('The goal with this dashboard is to simulate how stable pools would behave with different Amp Factors. It also aims to help the understanding of the impact of the Amp Factor and how Stable Pool works mathematically.')

st.write('If you want to understand more about Stable pools you can continue reading. If you want to use the simulation, feel free to change to the *stable curve page*')

st.write('*This dashboard was developed by [luizakp](https://github.com/luizakp) and [yvesfracari](https://github.com/yvesfracari)*')

st.header('Learning more about StablePool')

st.write('First of all, StablePools are the ones that performe StableSwaps, which is an Autonomous Market Maker (AMM) for stablecoins, meaning that **the price adjustment between the tokens is defined by a deterministic algorithm.** If you have the same input you will have the same output.')
st.write('StableSwaps are mathematically the combination between **constant sum formula** and **constant product formula (Uniswap)**')

st.subheader('Constant sum formula')

st.write('Here the constant is equal to the sum of the initial amount of tokens. So **x+y = k**. After a swap, the constant will remain the same, that will define the price and amount of token the user will receive in return of selling a certain amount of tokens.')
st.write('You will notice that with this formula the price is always 1, which there is no price impact but the pool can be completly drained.')
st.write('For a better understanding, please use this simulation:')

balance_x = st.number_input('Insert the initial amount of token X', value=2, step=1)
balance_y = st.number_input('Insert the initial amount of token Y', value=2, step=1)
x_data = {'name':'X', 'balance': balance_x}
y_data = {'name':'Y', 'balance': balance_y}
type_of_tokens = ['','X','Y']

linear_invariant = LinearInvariant(x=balance_x, y=balance_y)

st.write('K is equal to ', linear_invariant.constant)

type_token_sell = st.selectbox(label="Which token you want to sell?", options=type_of_tokens)

x = np.linspace(0, linear_invariant.constant)
y = np.linspace(0, linear_invariant.constant)

fig = px.line(x=x, y= linear_invariant.constant-x, title='Line Invariant Pool Chart')

if type_token_sell:
  tokens_data = linear_invariant.define_binary_sell_buy(type_token_sell, x_data, y_data)
  type_token_buy = tokens_data['type_token_buy']
  initial_amount_sell = tokens_data['initial_amount_sell']
  initial_amount_buy = tokens_data['initial_amount_buy']
  amount_token_sell = st.number_input(label='How much of token {} you want to sell?'.format(type_token_sell),value=2.0, step=0.1,max_value=float(initial_amount_buy), min_value=0.0)

  if amount_token_sell != 0 :
    transaction = linear_invariant.calculate_trade(initial_amount_sell, initial_amount_buy, amount_token_sell)
    amount_token_buy = transaction['amount_token_buy']
    st.write('You will receive', amount_token_buy, 'of token', type_token_buy)

    price = transaction['price']
    st.write('You paid 1 Y for', price, 'X')

    if type_token_sell == 'X':
        fig.add_scatter(mode="markers",x=transaction['transaction_sell'],y=transaction['transaction_buy'], text=transaction['label'],name="Transaction variation", hovertemplate='<br>'.join([
                '%{text}',
                'X: %{x}',
                'Y: %{y}',
            ]),
        )
    else:
        fig.add_scatter(mode="markers",x=transaction['transaction_buy'],y=transaction['transaction_sell'], text=transaction['label'],name="Transaction variation", hovertemplate='<br>'.join([
            '%{text}',
            'X: %{x}',
            'Y: %{y}',
        ]),
      )
  else: st.markdown(f'<p style="color:#C52233;">Please select the amount of token {type_token_sell} you want to sell</p>', unsafe_allow_html=True)
    
st.plotly_chart(fig, use_container_width=True)