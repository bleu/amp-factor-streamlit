import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.title('Linear Invariant')

amountX = st.number_input('Insert the initial amount of token X', value=2, step=1)
amountY = st.number_input('Insert the initial amount of token Y', value=2, step=1)

k = amountX+amountY

st.write('K is equal to ', k)

typeTokenSell = st.selectbox(label="Which token you want to sell?", options=['','X','Y'])

x = np.linspace(0, k)
y = np.linspace(0, k)

fig = px.line(x=x, y=k-x, title='Line Invariant Pool Chart')

if typeTokenSell:

  if typeTokenSell == 'X':
    typeTokenBuy = 'Y'
    initialAmountSell = amountX
    initialAmountBuy = amountY
    amountTokenSell = st.number_input(label='How much of token {} you want to sell?'.format(typeTokenSell),value=2, step=1,max_value=k-initialAmountBuy, min_value=0)

    if amountTokenSell != 0 :
      amountTokenBuy = initialAmountSell + initialAmountBuy + amountTokenSell - k
      st.write('You will receive', amountTokenBuy, 'of token', typeTokenBuy)

      price = amountTokenBuy/amountTokenSell
      st.write('You paid 1 Y for', price, 'X')

      finalAmountSell = initialAmountSell+amountTokenSell
      finalAmountBuy = initialAmountBuy-amountTokenBuy
      
      transaction = pd.DataFrame({
        'transactionSell': [initialAmountSell,finalAmountSell],
        'transactionBuy': [initialAmountBuy,finalAmountBuy],
        'label': ['Before the trade', 'After the trade']
      })

      fig.add_scatter(x=transaction['transactionSell'],y=transaction['transactionBuy'], text=transaction['label'],name="Transaction variation",        hovertemplate='<br>'.join([
              '%{text}',
              'X: %{x}',
              'Y: %{y}',
          ]),
      )
    else: st.markdown(f'<p style="color:#C52233;">Please select the amount of token {typeTokenSell} you want to sell</p>', unsafe_allow_html=True)
    

  if typeTokenSell == 'Y':
    typeTokenBuy = 'X'
    initialAmountSell = amountY
    initialAmountBuy = amountX
    amountTokenSell = st.number_input(label='How much of token {} you want to sell?'.format(typeTokenSell),value=2, step=1,max_value=k-initialAmountBuy, min_value=0)

    if amountTokenSell != 0 :
      amountTokenBuy = initialAmountSell + initialAmountBuy + amountTokenSell - k
      st.write('You will receive', amountTokenBuy, 'of token', typeTokenBuy)

      price = amountTokenBuy/amountTokenSell
      st.write('You paid 1Y for', price, 'X')

      finalAmountSell = initialAmountSell+amountTokenSell
      finalAmountBuy = initialAmountBuy-amountTokenBuy
      
      transaction = pd.DataFrame({
        'transactionSell': [initialAmountSell,finalAmountSell],
        'transactionBuy': [initialAmountBuy,finalAmountBuy],
        'label': ['Before the trade', 'After the trade']
      })

      fig.add_scatter(x=transaction['transactionBuy'],y=transaction['transactionSell'], text=transaction['label'],name="Transaction variation", hovertemplate='<br>'.join([
              '%{text}',
              'X: %{x}',
              'Y: %{y}',
          ]),
      )
    else: st.markdown(f'<p style="color:#C52233;">Please select the amount of token {typeTokenSell} you want to sell</p>', unsafe_allow_html=True)

st.plotly_chart(fig, use_container_width=True)

