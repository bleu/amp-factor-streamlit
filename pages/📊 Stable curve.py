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

if "pool_id" not in st.session_state:
  st.session_state["pool_data"] = {
    "pool_id": '0x2d011adf89f0576c9b722c28269fcb5d50c2d17900020000000000000000024d',
    "network": "Ethereum"
  }

networks = ["Ethereum", "Polygon", "Arbitrum"]
network = st.sidebar.selectbox('Network', options=networks, index=networks.index(st.session_state["pool_data"]["network"]))
pool_id = st.sidebar.text_input('Pool id', value=st.session_state["pool_data"]["pool_id"])

subgraph = Subgraph(network)
response = subgraph.query_pool_by_id(pool_id)
if response["pool"] is None:
  Components.error_container('Pool not found error', f'The pool {pool_id} do not exist in the {network} network')

elif response["pool"]["poolType"] != "Stable":
  Components.error_container('Not stable pool error', f'The {response["pool"]["name"]} pool is not stable')

else:
  st_utils = Streamlit()
  st_utils.initiate_session_state("pool_data", response["pool"])
  st_utils.initiate_session_state("x_data", st.session_state["pool_data"]["tokens"][0])
  st_utils.initiate_session_state("y_data", st.session_state["pool_data"]["tokens"][1])
  st_utils.initiate_session_state("names", [token["symbol"] for token in st.session_state["pool_data"]["tokens"]])
  st_utils.initiate_session_state("balances", [float(token["balance"]) for token in st.session_state["pool_data"]["tokens"]])
  st_utils.initiate_session_state("pool", {"pool_id": pool_id, "network": network})

  st.title(f'{st.session_state["pool_data"]["name"]} Simulation')
  col1, col2 = st.columns(2)

  base_x = float(st.session_state["x_data"]["balance"])
  base_y = float(st.session_state["y_data"]["balance"])
  base_amp = float(st.session_state["pool_data"]["amp"])
  amp_series = base_amp*np.append(np.logspace(-3, 0, endpoint=False), np.logspace(0, 3))

  balance = px.pie(values=st.session_state["balances"], names=st.session_state["names"], labels=st.session_state["names"])
  balance.update_traces(hovertemplate='<b>%{value}</b>')
  balance.update_layout(title="Tokens distribution")
  st.sidebar.plotly_chart(balance, use_container_width=True)
  st.sidebar.write('Base Amp Factor :', base_amp)
  new_amp = st.sidebar.select_slider('Amp factor', options=amp_series, value=base_amp)
  type_token_sell = st.sidebar.selectbox(label="Which token you want to sell?", options=st.session_state["names"])

  col1.header("Depth Cost")

  pool = StableSwapBinary(x=st.session_state["balances"][0], y=st.session_state["balances"][1], amp=base_amp)
  new_pool = StableSwapBinary(x=st.session_state["balances"][0], y=st.session_state["balances"][1], amp=new_amp)

  dfs = []

  if type_token_sell:
    # hardcoded for binary pool
    input_token_index = st.session_state["names"].index(type_token_sell)
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
    depth_fig = px.bar(df, x='Pair token', y="Cost", color="Amp factor", facet_col="Price change", barmode="group")
    title = "2% Depth Cost Analysis for {}".format(type_token_sell)
    depth_fig.update_layout(title=title, yaxis_title=type_token_sell)
    col1.plotly_chart(depth_fig, use_container_width=True)

  

  html_components = Components()
  st.header("Pool")

  current_stable_swape = StableSwapBinary(x=base_x, y=base_y, amp=base_amp)
  new_stable_swape = StableSwapBinary(x=base_x, y=base_y, amp=new_amp)
  linear_invariant = LinearInvariant(x=base_x, y=base_y)

  df = pd.DataFrame()

  x_data_name = st.session_state["x_data"]["name"]
  df[x_data_name] = np.linspace(linear_invariant.constant*0.2, linear_invariant.constant*0.8, num=100)
  df["Current curve"] = current_stable_swape.calculate_y(df[x_data_name])
  df["New curve"] = new_stable_swape.calculate_y(df[x_data_name])

  df["Current spot price"] = current_stable_swape.calculate_spot_price(df[x_data_name])
  df["New spot price"] = new_stable_swape.calculate_spot_price(df[x_data_name])

  pool_fig = go.Figure(go.Scatter(
      name = "Default Amp Factor",
      x = df[x_data_name],
      y = df["Current curve"],
      hovertemplate =
      '<b>Price: %{text}</b>',
      text = df["Current spot price"].map('{:.5f}'.format)))

  pool_fig.add_trace(go.Scatter(
      name = "New Amp Factor",
      x = df[x_data_name],
      y = df["New curve"],
      hovertemplate = '<b>Price: %{text}</b>',
      text = df["New spot price"].map('{:.5f}'.format)))

  pool_fig.update_layout(hovermode='x unified')

  if type_token_sell:
    tokens_data = new_stable_swape.define_binary_sell_buy(type_token_sell, st.session_state["x_data"], st.session_state["y_data"])
    type_token_buy = tokens_data['type_token_buy']
    initial_amount_sell = tokens_data['initial_amount_sell']
    initial_amount_buy = tokens_data['initial_amount_buy']
    amount_token_sell = st.sidebar.number_input(label='How much of token {} you want to sell?'.format(type_token_sell),value=400.00, step=0.1,max_value=float(initial_amount_buy), min_value=0.0)
    
    new_transaction = new_stable_swape.calculate_trade(initial_amount_sell, initial_amount_buy, amount_token_sell)
    current_transaction = current_stable_swape.calculate_trade(initial_amount_sell, initial_amount_buy, amount_token_sell)
    new_amount_token_buy = new_transaction['amount_token_buy']

    current_amp = {'amp':base_amp, 'type_token_buy': type_token_buy, 'amount_token_buy':current_transaction['amount_token_buy'], 'price':current_transaction['price'], 'default_price':current_transaction['price'] }
    custom_amp = {'amp':new_amp, 'type_token_buy': type_token_buy, 'amount_token_buy':new_transaction['amount_token_buy'], 'price':new_transaction['price'], 'default_price':current_transaction['price'] }

    html_components.amp_price_conteiner(current_amp,custom_amp, type_token_sell)

    if type_token_sell == st.session_state["x_data"]["name"]:
      pool_fig.add_scatter(mode="markers",x=current_transaction['transaction_sell'],y=current_transaction['transaction_buy'], text=current_transaction['label'],name="", hovertemplate='%{x} ; %{y}',        
        marker=dict(
            color='#2533F8',
            size=7,
        ), showlegend=False)
      pool_fig.add_scatter(mode="markers",x=new_transaction['transaction_sell'],y=new_transaction['transaction_buy'], text=new_transaction['label'],name="", hovertemplate='%{x} ; %{y}',           
        marker=dict(
            color='#ED3C1D',
            size=7,
        ), showlegend=False)
    if type_token_sell == st.session_state["y_data"]["name"]:
      pool_fig.add_scatter(mode="markers",x=current_transaction['transaction_buy'],y=current_transaction['transaction_sell'], text=current_transaction['label'],name="", hovertemplate='%{x} ; %{y}',       
        marker=dict(
            color='#2533F8',
            size=7,
        ), showlegend=False)
      pool_fig.add_scatter(mode="markers",x=new_transaction['transaction_buy'],y=new_transaction['transaction_sell'], text=new_transaction['label'],name="", hovertemplate='%{x} ; %{y}',         
        marker=dict(
            color='#ED3C1D',
            size=7,
        ), showlegend=False)

  pool_fig.update_layout(yaxis_title=st.session_state["y_data"]["name"])

  st.plotly_chart(pool_fig, use_container_width=True)
