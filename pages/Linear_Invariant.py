import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.title('Linear Invariant')

amountX = st.number_input('Insert the amount of token X', value=2, step=1)
amountY = st.number_input('Insert the amount of token Y', value=2, step=1)

k = amountX+amountY

st.write('K is equal to ', k)

x = np.linspace(0, k)
y = np.linspace(0, k)

fig = px.line(x=x, y=k-x, title='Line Invariant Chart')

st.plotly_chart(fig, use_container_width=True)