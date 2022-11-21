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

if typeTokenSell:
  amounTokenSell = st.number_input(label='How much of token {} you want to sell?'.format(typeTokenSell),value=2, step=1,max_value=k, min_value=0)

  if typeTokenSell == 'X':
    typeTokenBuy = 'Y'
    initialAmountSell = amountX
    initialAmountBuy = amountY
    amountTokenBuy = initialAmountSell + initialAmountBuy + amounTokenSell - k
    st.write('You will receive', amountTokenBuy, 'of token', typeTokenBuy)
    st.write('You will receive', amountTokenBuy, 'of token', typeTokenBuy)



x = np.linspace(0, k)
y = np.linspace(0, k)

fig = px.line(x=x, y=k-x, title='Line Invariant Chart')

st.plotly_chart(fig, use_container_width=True)

