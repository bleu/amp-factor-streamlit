import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.queries import Subgraph
from utils.market_makers import LinearInvariant, Uniswap, StableSwap

st.title('Stable curve simulation')
pool_id = st.text_input('Pool id', value='0x2d011adf89f0576c9b722c28269fcb5d50c2d17900020000000000000000024d')

subgraph = Subgraph()
response = subgraph.query_pool_by_id(pool_id)
pool_data = response["pool"]
x_data = pool_data["tokens"][0]
y_data = pool_data["tokens"][1]

st.subtitle(pool_data["name"])

base_x = float(x_data["balance"])
base_y = float(x_data["balance"])
base_amp = float(x_data["balance"])

amountAmp = st.slider('Amp factor', min_value=base_amp/100, max_value=base_amp*2, value=base_amp, step=base_amp/100)

stable_swape = StableSwap(x=base_x, y=base_y, amp=base_amp)
linear_invariant = LinearInvariant(x=base_x, y=base_y)
uniswap = Uniswap(x=base_x, y=base_y)

st.write('Constant value of the pool is equal to ', stable_swape.constant)

df = pd.DataFrame()

df[x_data["name"]] = np.linspace(linear_invariant.constant/1000, linear_invariant.constant, num=1000)
df["StableSwap"] = stable_swape.calculate_y(df[x_data["name"]], amountAmp)
df["Linear Invariant"] = linear_invariant.calculate_y(df[x_data["name"]])

df["Uniswap"] = uniswap.calculate_y(df[x_data["name"]])
df["Price StableSwap"] = df["StableSwap"] / df[x_data["name"]]
df["Price Linear Invariant"] = df["Linear Invariant"] / df[x_data["name"]]
df["Price Uniswap"] = df["Uniswap"] / df[x_data["name"]]

fig = px.line(df, x=x_data["name"], y=["StableSwap", "Linear Invariant", "Uniswap"], 
              hover_data=["Price StableSwap", "Price Linear Invariant", "Price Uniswap"], title='StableSwap plot')

fig.update_layout(yaxis_title=y_data["name"])

st.plotly_chart(fig, use_container_width=True)