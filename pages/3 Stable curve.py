import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.queries import Subgraph
from utils.market_makers import LinearInvariant, Uniswap, StableSwapBinary
from utils.html_components import Components

html_components = Components()
st.title('Stable curve simulation')
pool_id = st.text_input('Pool id', value='0x2d011adf89f0576c9b722c28269fcb5d50c2d17900020000000000000000024d')

if st.session_state.get("pool_id") != pool_id:
  subgraph = Subgraph()
  response = subgraph.query_pool_by_id(pool_id)
  st.session_state["pool_data"] = response["pool"]
  st.session_state["x_data"] = st.session_state["pool_data"]["tokens"][0]
  st.session_state["y_data"] = st.session_state["pool_data"]["tokens"][1]
  st.session_state["pool_id"] = pool_id

st.header(st.session_state["pool_data"]["name"])

base_x = float(st.session_state["x_data"]["balance"])
base_y = float(st.session_state["y_data"]["balance"])
base_amp = float(st.session_state["pool_data"]["amp"])

html_components.binary_balance_conteiner(st.session_state["x_data"],st.session_state["y_data"])

amp_series = base_amp*np.append(np.logspace(-3, 0, endpoint=False), np.logspace(0, 3))

amountAmp = st.select_slider('Amp factor', options=amp_series, value=base_amp)

current_stable_swape = StableSwapBinary(x=base_x, y=base_y, amp=base_amp)
new_stable_swape = StableSwapBinary(x=base_x, y=base_y, amp=amountAmp)
linear_invariant = LinearInvariant(x=base_x, y=base_y)

df = pd.DataFrame()

x_data_name = st.session_state["x_data"]["name"]
df[x_data_name] = np.linspace(linear_invariant.constant*0.2, linear_invariant.constant*0.8, num=100)
df["Current curve"] = current_stable_swape.calculate_y(df[x_data_name])
df["New curve"] = new_stable_swape.calculate_y(df[x_data_name])
df["Linear invariant"] = linear_invariant.calculate_y(df[x_data_name])

df["Current spot price"] = current_stable_swape.calculate_spot_price(df[x_data_name])
df["New spot price"] = new_stable_swape.calculate_spot_price(df[x_data_name])

fig = px.line(df, x=x_data_name, y=["Current curve", "New curve", "Linear invariant"], 
              hover_data=["Current spot price", "New spot price"], title='StableSwap simulation')

fig.update_layout(yaxis_title=st.session_state["y_data"]["name"])

st.plotly_chart(fig, use_container_width=True)
