import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.queries import Subgraph
from utils.market_makers import StableSwap
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
  st.session_state["pool_id"] = '0x06df3b2bbb68adc8b0e302443692037ed9f91b42000000000000000000000063'
  
pool_id = st.text_input('Pool id', value=st.session_state["pool_id"])

subgraph = Subgraph()
st_utils = Streamlit()
html_components = Components()
response = subgraph.query_pool_by_id(pool_id)
st_utils.initiate_session_state("pool_data", response["pool"])
st_utils.initiate_session_state("tokens", response["pool"]["tokens"])
st_utils.initiate_session_state("tokens_names", [t["name"] for t in response["pool"]["tokens"]])
st_utils.initiate_session_state("tokens_balances", [float(t["balance"]) for t in response["pool"]["tokens"]])
base_amp = float(st.session_state["pool_data"]["amp"])
amp_series = base_amp*np.append(np.logspace(-3, 0, endpoint=False), np.logspace(0, 3))
amountAmp = st.select_slider('Amp factor', options=amp_series, value=base_amp)
type_token_sell = st.selectbox(label="Which token you want to sell?", options=st.session_state["tokens_names"])
token_to_sell_index = st.session_state["tokens_names"].index(type_token_sell)
other_tokens_index = [i for i in range(len(st.session_state["tokens_names"])) if i != token_to_sell_index]

st_utils.initiate_session_state("x_data", st.session_state["pool_data"]["tokens"][token_to_sell_index])
st_utils.initiate_session_state("y_data", [st.session_state["pool_data"]["tokens"][i] for i in other_tokens_index])
st_utils.initiate_session_state("pool_id", pool_id)
amount_token_sell = st.number_input(label='How much of token {} you want to sell?'.format(type_token_sell),value=400.00, step=0.1,max_value=float(st.session_state["x_data"]["balance"]), min_value=0.0)

st.header(st.session_state["pool_data"]["name"])

tabs = st.tabs([y_data["name"] for y_data in st.session_state["y_data"]])
for index in range(len(st.session_state["y_data"])):
  with tabs[index]:
    y_data = st.session_state["y_data"][index]
    base_x = float(st.session_state["x_data"]["balance"])
    base_y = float(y_data["balance"])

    current_stable_swape = StableSwap(names=st.session_state["tokens_names"], amp=base_amp, balances=st.session_state["tokens_balances"])
    new_stable_swape = StableSwap(names=st.session_state["tokens_names"], amp=amountAmp, balances=st.session_state["tokens_balances"])

    df = pd.DataFrame()

    x_data_name = st.session_state["x_data"]["name"]
    df[x_data_name] = np.linspace(float(current_stable_swape.constant)*0.2, float(current_stable_swape.constant)*0.8, num=100)
    df["Current curve"] = df[x_data_name].apply(lambda x: current_stable_swape.calculate_y(type_token_sell, y_data["name"], x)) 
    df["New curve"] = df[x_data_name].apply(lambda x: new_stable_swape.calculate_y(type_token_sell, y_data["name"], x))

    df["Current spot price"] = df[x_data_name].apply(lambda x: current_stable_swape.calculate_spot_price(type_token_sell, y_data["name"], x))
    df["New spot price"] = df[x_data_name].apply(lambda x: new_stable_swape.calculate_spot_price(type_token_sell, y_data["name"], x))


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

    type_token_buy = y_data["name"]
    new_transaction = new_stable_swape.calculate_trade(type_token_sell, y_data["name"], amount_token_sell)
    current_transaction = current_stable_swape.calculate_trade(type_token_sell, y_data["name"], amount_token_sell)
    new_amount_token_buy = new_transaction['amount_token_buy']

    current_amp = {'amp':base_amp, 'type_token_buy': y_data["name"], 'amount_token_buy':current_transaction['amount_token_buy'], 'price':current_transaction['price'], 'default_price':current_transaction['price'] }
    new_amp = {'amp':amountAmp, 'type_token_buy': y_data["name"], 'amount_token_buy':new_transaction['amount_token_buy'], 'price':new_transaction['price'], 'default_price':current_transaction['price'] }

    html_components.amp_price_conteiner(current_amp,new_amp)

    #todo find a better way to to this hover
    hover = "<br>%{text}<br>"
    hover += "{}: ".format(st.session_state["x_data"]["name"])
    hover += "<b>%{x}</b><br>"
    hover += "{}: ".format(y_data["name"])
    hover += "<b>%{y}</b><br>"

    st.write('You paid',new_transaction['price'], y_data["name"], 'for 1',  st.session_state["x_data"]["name"])
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

    fig.update_layout(yaxis_title=y_data["name"])

    st.plotly_chart(fig, use_container_width=True)