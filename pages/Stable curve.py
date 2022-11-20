import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

subgraph_url = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2"
balancer_transport=RequestsHTTPTransport(
    url=subgraph_url,
    verify=True,
    retries=3
)
client = Client(transport=balancer_transport)

def get_D_binary_pool(x, y, amp):
  a = 1/4
  b = amp
  c = -1 * ((amp * (x+y)) + (x*y))
  delta = ((b**2) - (4*a*c))**(1/2) 
  return (-b + delta)/(2*a)

def get_y_binary_pool(x, amp, D):
  first_part = amp*D + ((D**2)/4) - amp*x
  second_part = (amp+x)**(-1)
  return first_part * second_part

def query_pool_data(pool_id):
  query = '''
  query {{
      pools(where: {{ id: "{pool_id}" }}) {{
          amp
          name
      }}
      poolTokens( where: {{ poolId: "{pool_id}" }}) {{
          id
              name
              balance
      }}
  }}
  '''
  return client.execute(gql(query.format(pool_id=pool_id)))

st.title('Stable curve simulation')
pool_id = st.text_input('Pool id', value='0x2d011adf89f0576c9b722c28269fcb5d50c2d17900020000000000000000024d')

response = query_pool_data(pool_id)
pool_data = response["pools"][0]
x_data = response["poolTokens"][0]
y_data = response["poolTokens"][1]

st.write('Pool Name: ', pool_data["name"])

base_x = float(x_data["balance"])
base_y = float(x_data["balance"])
base_amp = float(x_data["balance"])

amountX = st.slider(x_data["name"], min_value=base_x/100, max_value=base_x*2, value=base_x, step=base_x/100)
amountY = st.slider(y_data["name"], min_value=base_y/100, max_value=base_y*2, value=base_y, step=base_y/100)
amountAmp = st.slider('Amp factor', min_value=base_amp/100, max_value=base_amp*2, value=base_amp, step=base_amp/100)

D = get_D_binary_pool(amountX, amountY, amountAmp)

st.write('D is equal to ', D)

df = pd.DataFrame()

df[x_data["name"]] = np.linspace(amountX/2, 2*amountX, num=1000)
df[y_data["name"]] = get_y_binary_pool(df[x_data["name"]], amountAmp, D)
df["Price"] = df[y_data["name"]] / df[x_data["name"]]

fig = px.line(df, x=x_data["name"], y=y_data["name"], hover_data=["Price"], title='StableSwap plot')

st.plotly_chart(fig, use_container_width=True)