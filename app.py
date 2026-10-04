import streamlit as st

st.set_page_config(page_title="LipiSetu", page_icon="🌉", layout="centered")

st.title("LipiSetu")

name = st.text_input("Your name")
if st.button("Submit"):
    st.write(f"Welcome{name}!")