import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.title('Constant product formula')

amountX = st.number_input('Insert the initial amount of token X', value=10, step=1)
amountY = st.number_input('Insert the initial amount of token Y', value=10, step=1)

k = amountX*amountY

st.write('K is equal to ', k)

typeTokenSell = st.selectbox(label="Which token you want to sell?", options=['','X','Y'])

x = np.linspace(0, k,num=k)
y = np.linspace(0, k,num=k)

fig = px.line(x=x, y=(k/x), title='Constant product formula Pool Chart')

if typeTokenSell:

  if typeTokenSell == 'X':
    typeTokenBuy = 'Y'
    initialAmountSell = amountX
    initialAmountBuy = amountY
    amountTokenSell = st.number_input(label='How much of token {} you want to sell?'.format(typeTokenSell),value=2.0, step=0.1,max_value=float(k), min_value=0.1)

    if amountTokenSell != 0 :
      amountTokenBuy = (initialAmountBuy*amountTokenSell)/(initialAmountSell+amountTokenSell)
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

      fig.add_scatter(mode="markers",x=transaction['transactionSell'],y=transaction['transactionBuy'], text=transaction['label'],name="Transaction variation",        hovertemplate='<br>'.join([
              '%{text}',
              'X: %{x}',
              'Y: %{y}',
          ]),
      )
      x = np.linspace(0, finalAmountSell)
    else: st.markdown(f'<p style="color:#C52233;">Please select the amount of token {typeTokenSell} you want to sell</p>', unsafe_allow_html=True)
  
  if typeTokenSell == 'Y':
    typeTokenBuy = 'X'
    initialAmountSell = amountY
    initialAmountBuy = amountX
    amountTokenSell = st.number_input(label='How much of token {} you want to sell?'.format(typeTokenSell),value=2.0, step=0.1,max_value=float(k), min_value=0.1)

    if amountTokenSell != 0 :
      amountTokenBuy = (initialAmountBuy*amountTokenSell)/(initialAmountSell+amountTokenSell)
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

      fig.add_scatter(mode="markers",x=transaction['transactionBuy'],y=transaction['transactionSell'], text=transaction['label'],name="Transaction variation",        hovertemplate='<br>'.join([
              '%{text}',
              'X: %{x}',
              'Y: %{y}',
          ]),
      )
    else: st.markdown(f'<p style="color:#C52233;">Please select the amount of token {typeTokenSell} you want to sell</p>', unsafe_allow_html=True)

st.plotly_chart(fig, use_container_width=True)