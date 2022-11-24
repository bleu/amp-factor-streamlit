import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.queries import Subgraph
from utils.market_makers import LinearInvariant, Uniswap, StableSwapBinary

st.title('Stable curve simulation')
pool_id = st.text_input('Pool id', value='0x2d011adf89f0576c9b722c28269fcb5d50c2d17900020000000000000000024d')

subgraph = Subgraph()
response = subgraph.query_pool_by_id(pool_id)
pool_data = response["pool"]
x_data = pool_data["tokens"][0]
y_data = pool_data["tokens"][1]

st.header(pool_data["name"])

base_x = float(x_data["balance"])
base_y = float(x_data["balance"])
base_amp = float(x_data["balance"])

amountAmp = st.slider('Amp factor', min_value=base_amp/100, max_value=base_amp*2, value=base_amp, step=base_amp/100)

stable_swape = StableSwapBinary(x=base_x, y=base_y, amp=amountAmp)
linear_invariant = LinearInvariant(x=base_x, y=base_y)

df = pd.DataFrame()

df[x_data["name"]] = np.linspace(linear_invariant.constant/1000, linear_invariant.constant, num=1000)
df["StableSwap"] = stable_swape.calculate_y(df[x_data["name"]])
df["Linear Invariant"] = linear_invariant.calculate_y(df[x_data["name"]])

df["SpotPrice StableSwap"] = stable_swape.calculate_spot_price(df[x_data["name"]])
df["SpotPrice Linear Invariant"] = linear_invariant.calculate_spot_price()

fig = px.line(df, x=x_data["name"], y=["StableSwap", "Linear Invariant"], 
              hover_data=["SpotPrice StableSwap", "SpotPrice Linear Invariant"], title='StableSwap plot')

fig.update_layout(yaxis_title=y_data["name"])

st.plotly_chart(fig, use_container_width=True)