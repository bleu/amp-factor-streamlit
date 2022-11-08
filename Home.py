import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Amp Factor Dashboard')

yRange = st.slider('y', 0, 130, 10)

number = st.number_input('Insert a number')
x = np.linspace(number-6, number+6)
y = np.linspace(yRange-6, yRange+6)
fig = px.line(x=x, y=y*x, title='Line chart test')

st.plotly_chart(fig, use_container_width=True)