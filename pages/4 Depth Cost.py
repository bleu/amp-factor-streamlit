import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.queries import Subgraph
from utils.market_makers import StableSwapBinary

st.title("Depth Cost")

pool_id = st.text_input('Pool id', value='0x2d011adf89f0576c9b722c28269fcb5d50c2d17900020000000000000000024d')

if st.session_state.get("pool_id") != pool_id:
  subgraph = Subgraph()
  response = subgraph.query_pool_by_id(pool_id)
  st.session_state["pool_data"] = response["pool"]
  st.session_state["balances"] = [float(token["balance"]) for token in st.session_state["pool_data"]["tokens"]]
  st.session_state["names"] = [token["name"] for token in st.session_state["pool_data"]["tokens"]]
  st.session_state["pool_id"] = pool_id
  st.session_state["names"].reverse()

st.header(st.session_state["pool_data"]["name"])

base_amp = float(st.session_state["pool_data"]["amp"])

cost_depth_percentage = st.slider("Cost Depth (%):", min_value=0, max_value=100, value=20)
amp_serie = base_amp*np.append(np.logspace(-3, 0, endpoint=False), np.logspace(0, 3))
new_amp = st.select_slider('Amp factor', options=amp_serie, value=base_amp)

pool = StableSwapBinary(x=st.session_state["balances"][0], y=st.session_state["balances"][1], amp=base_amp)
new_pool = StableSwapBinary(x=st.session_state["balances"][0], y=st.session_state["balances"][1], amp=new_amp)

dfs = []

for p, tag, amp in zip([pool, new_pool], ["Current", "New"], [base_amp, new_amp]):
  df = pd.DataFrame()
  df["Input token"] = st.session_state["names"]
  df["Balance"] = st.session_state["balances"]
  df["Amp factor tag"] = tag
  df["Amp factor value"] = amp
  df["Current price"] = p.calculate_spot_price(df["Balance"])
  df["Target price"] = df["Current price"]*(1-(cost_depth_percentage/100))
  df["Value for 2% Depth"] = p.calculate_value_to_spot_price(df["Balance"], df["Target price"])
  dfs.append(df)

df = pd.concat(dfs)
fig = px.bar(df, x='Input token', y="Value for 2% Depth", color="Amp factor tag", barmode="group")
st.plotly_chart(fig, use_container_width=True)
