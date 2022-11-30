import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.market_makers import LinearInvariant

st.title('Linear Invariant')

balanceX = st.number_input('Insert the initial amount of token X', value=2, step=1)
balanceY = st.number_input('Insert the initial amount of token Y', value=2, step=1)

linear_invariant = LinearInvariant(x=balanceX, y=balanceY)

k = linear_invariant.get_constant(balanceX,balanceY)

st.write('K is equal to ', k)

typeTokenSell = st.selectbox(label="Which token you want to sell?", options=['','X','Y'])

x = np.linspace(0, k)
y = np.linspace(0, k)

fig = px.line(x=x, y=k-x, title='Line Invariant Pool Chart')

if typeTokenSell:
  tokensData = linear_invariant.define_sell_buy(typeTokenSell,balanceX,balanceY)
  typeTokenBuy = tokensData['typeTokenBuy']
  initialAmountSell = tokensData['initialAmountSell']
  initialAmountBuy = tokensData['initialAmountBuy']
  amountTokenSell = st.number_input(label='How much of token {} you want to sell?'.format(typeTokenSell),value=2.0, step=0.1,max_value=float(initialAmountBuy), min_value=0.0)

  if amountTokenSell != 0 :
    transaction = linear_invariant.calculate_trade(initialAmountSell, initialAmountBuy, amountTokenSell)
    amountTokenBuy = transaction['amountTokenBuy']
    st.write('You will receive', amountTokenBuy, 'of token', typeTokenBuy)

    price = transaction['price']
    st.write('You paid 1 Y for', price, 'X')

    if typeTokenSell == 'X':
        fig.add_scatter(mode="markers",x=transaction['transactionSell'],y=transaction['transactionBuy'], text=transaction['label'],name="Transaction variation", hovertemplate='<br>'.join([
                '%{text}',
                'X: %{x}',
                'Y: %{y}',
            ]),
        )
    if typeTokenSell == 'Y':
        fig.add_scatter(mode="markers",x=transaction['transactionBuy'],y=transaction['transactionSell'], text=transaction['label'],name="Transaction variation", hovertemplate='<br>'.join([
            '%{text}',
            'X: %{x}',
            'Y: %{y}',
        ]),
      )
  else: st.markdown(f'<p style="color:#C52233;">Please select the amount of token {typeTokenSell} you want to sell</p>', unsafe_allow_html=True)
    
st.plotly_chart(fig, use_container_width=True)

