import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.market_makers import LinearInvariant

st.title('Linear Invariant')

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
    st.write('You paid', price,'Y for 1 X')

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

