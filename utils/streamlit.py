import streamlit as st

class Streamlit:
  def initiate_session_state(self, key, value):
    if key not in st.session_state:
      st.session_state[key] = value  