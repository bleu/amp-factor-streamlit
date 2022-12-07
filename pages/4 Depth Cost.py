import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.queries import Subgraph
from utils.market_makers import StableSwapBinary
from utils.streamlit import Streamlit

st.title("Depth Cost")

## tem alguma variavel sendo compartilhada entre as duas páginas e por isso da dando ruim
if "pool_id" not in st.session_state:
  st.session_state["pool_id"] = '0x2d011adf89f0576c9b722c28269fcb5d50c2d17900020000000000000000024d'

pool_id_depth_cost = st.text_input('Pool id', value=st.session_state["pool_id"])

subgraph = Subgraph()
response = subgraph.query_pool_by_id(pool_id_depth_cost)
st_utils = Streamlit()
st_utils.initiate_session_state("pool_data_depth_cost", response["pool"])
st_utils.initiate_session_state("names", [token["name"] for token in st.session_state["pool_data_depth_cost"]["tokens"]])
st_utils.initiate_session_state("balances", [float(token["balance"]) for token in st.session_state["pool_data_depth_cost"]["tokens"]])
st_utils.initiate_session_state("pool_id", pool_id_depth_cost)

st.header(st.session_state["pool_data_depth_cost"]["name"])

base_amp = float(st.session_state["pool_data_depth_cost"]["amp"])

input_token = st.selectbox("Select the input token:", st.session_state["names"])
amp_serie = base_amp*np.append(np.logspace(-3, 0, endpoint=False), np.logspace(0, 3))
new_amp = st.select_slider('Amp factor', options=amp_serie, value=base_amp)

pool = StableSwapBinary(x=st.session_state["balances"][0], y=st.session_state["balances"][1], amp=base_amp)
new_pool = StableSwapBinary(x=st.session_state["balances"][0], y=st.session_state["balances"][1], amp=new_amp)

dfs = []

# hardcoded for binary pool
input_token_index = st.session_state["names"].index(input_token)
indexes_to_plot = [i for i in range(len(st.session_state["names"])) if i != input_token_index]

for p, amp_tag, amp in zip([pool, new_pool], ["Current", "New"], [base_amp, new_amp]):
  for price_tag, price in zip(["-2%", "+2%"], [-2, 2]):
    df = pd.DataFrame()
    df["Pair token"] = np.array(st.session_state["names"])[indexes_to_plot]
    df["Balance"] = np.array(st.session_state["balances"])[indexes_to_plot]
    df["Amp factor"] = amp_tag
    df["Amp factor value"] = amp

    # considering 2 percentage of cost change
    df["Current price"] = p.calculate_spot_price(df["Balance"])
    df["Price change"] = price_tag
    df["Price Target"] = df["Current price"]*(1+(price/100))
    df["Cost"] = p.calculate_value_to_spot_price(df["Balance"], df["Price Target"])
    dfs.append(df)

df = pd.concat(dfs)
fig = px.bar(df, x='Pair token', y="Cost", color="Amp factor", facet_col="Price change", barmode="group")
title = "2% Depth Cost Analysis for {}".format(input_token)
fig.update_layout(title=title, yaxis_title=input_token)
st.plotly_chart(fig, use_container_width=True)
