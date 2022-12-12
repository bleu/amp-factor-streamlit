import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.queries import Subgraph
from utils.market_makers import LinearInvariant, Uniswap, StableSwapBinary
from utils.streamlit import Streamlit
from utils.html_components import Components

st.set_page_config(
   page_title="Simulation | Amp Factor",
   page_icon="📊",
   initial_sidebar_state="expanded",
   layout="wide",
)

st.title('Stable curve simulation')
if "pool_id" not in st.session_state:
  st.session_state["pool_id"] = '0x2d011adf89f0576c9b722c28269fcb5d50c2d17900020000000000000000024d'
  
pool_id = st.text_input('Pool id', value=st.session_state["pool_id"])

subgraph = Subgraph()
response = subgraph.query_pool_by_id(pool_id)
st_utils = Streamlit()
st_utils.initiate_session_state("pool_data", response["pool"])
st_utils.initiate_session_state("x_data", st.session_state["pool_data"]["tokens"][0])
st_utils.initiate_session_state("y_data", st.session_state["pool_data"]["tokens"][1])
st_utils.initiate_session_state("pool_id", pool_id)

st.header(st.session_state["pool_data"]["name"])

base_x = float(st.session_state["x_data"]["balance"])
base_y = float(st.session_state["y_data"]["balance"])
base_amp = float(st.session_state["pool_data"]["amp"])
type_of_tokens = ['',f'{st.session_state["x_data"]["name"]}',f'{st.session_state["y_data"]["name"]}']

html_components = Components()
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

df["Current spot price"] = current_stable_swape.calculate_spot_price(df[x_data_name])
df["New spot price"] = new_stable_swape.calculate_spot_price(df[x_data_name])

type_token_sell = st.selectbox(label="Which token you want to sell?", options=type_of_tokens)

fig = go.Figure(go.Scatter(
    name = "Default Amp Factor",
    x = df[x_data_name],
    y = df["Current curve"],
    hovertemplate =
    '<b>Price: %{text}</b>',
    text = df["Current spot price"].map('{:.5f}'.format)))

fig.add_trace(go.Scatter(
    name = "New Amp Factor",
    x = df[x_data_name],
    y = df["New curve"],
    hovertemplate = '<b>Price: %{text}</b>',
    text = df["New spot price"].map('{:.5f}'.format)))

fig.update_layout(hovermode='x unified')

if type_token_sell:
  tokens_data = new_stable_swape.define_binary_sell_buy(type_token_sell, st.session_state["x_data"], st.session_state["y_data"])
  type_token_buy = tokens_data['type_token_buy']
  initial_amount_sell = tokens_data['initial_amount_sell']
  initial_amount_buy = tokens_data['initial_amount_buy']
  amount_token_sell = st.number_input(label='How much of token {} you want to sell?'.format(type_token_sell),value=400.00, step=0.1,max_value=float(initial_amount_buy), min_value=0.0)

  if amount_token_sell != 0 :
    new_transaction = new_stable_swape.calculate_trade(initial_amount_sell, initial_amount_buy, amount_token_sell)
    current_transaction = current_stable_swape.calculate_trade(initial_amount_sell, initial_amount_buy, amount_token_sell)
    new_amount_token_buy = new_transaction['amount_token_buy']

    current_amp = {'amp':base_amp, 'type_token_buy': type_token_buy, 'amount_token_buy':current_transaction['amount_token_buy'], 'price':current_transaction['price'], 'default_price':current_transaction['price'] }
    new_amp = {'amp':amountAmp, 'type_token_buy': type_token_buy, 'amount_token_buy':new_transaction['amount_token_buy'], 'price':new_transaction['price'], 'default_price':current_transaction['price'] }

    html_components.amp_price_conteiner(current_amp,new_amp)

    #todo find a better way to to this hover
    hover = "<br>%{text}<br>"
    hover += "{}: ".format(st.session_state["x_data"]["name"])
    hover += "<b>%{x}</b><br>"
    hover += "{}: ".format(st.session_state["y_data"]["name"])
    hover += "<b>%{y}</b><br>"

    if type_token_sell == st.session_state["x_data"]["name"]:
      st.write('You paid',new_transaction['price'], st.session_state["y_data"]["name"], 'for 1',  st.session_state["x_data"]["name"])
      fig.add_scatter(mode="markers",x=current_transaction['transaction_sell'],y=current_transaction['transaction_buy'], text=current_transaction['label'],name="", hovertemplate=hover,         
        marker=dict(
            color='#2533F8',
            size=7,
        ), showlegend=False)
      fig.add_scatter(mode="markers",x=new_transaction['transaction_sell'],y=new_transaction['transaction_buy'], text=new_transaction['label'],name="",hovertemplate=hover,         
        marker=dict(
            color='#ED3C1D',
            size=7,
        ), showlegend=False)
    if type_token_sell == st.session_state["y_data"]["name"]:
      st.write('You paid 1', st.session_state["x_data"]["name"], 'for', new_transaction['price'],  st.session_state["y_data"]["name"])
      fig.add_scatter(mode="markers",x=current_transaction['transaction_buy'],y=current_transaction['transaction_sell'], text=current_transaction['label'],name="", hovertemplate=hover,         
        marker=dict(
            color='#2533F8',
            size=7,
        ), showlegend=False)
      fig.add_scatter(mode="markers",x=new_transaction['transaction_buy'],y=new_transaction['transaction_sell'], text=new_transaction['label'],name="",hovertemplate=hover,         
        marker=dict(
            color='#ED3C1D',
            size=7,
        ), showlegend=False)

fig.update_layout(yaxis_title=st.session_state["y_data"]["name"])

st.plotly_chart(fig, use_container_width=True)