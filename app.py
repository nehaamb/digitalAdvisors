# app.py

import streamlit as st

st.title("Streamlit App Inside JupyterLab")
name = st.text_input("Enter your name")
if name:
    st.write(f"Hello, {name} 👋")
