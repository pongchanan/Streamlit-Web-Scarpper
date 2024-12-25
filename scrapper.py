import streamlit as st

st.markdown("<h1 style='text-align: center'>Web scrapper</h1>", unsafe_allow_html=True)

with st.form("Search"):
    keyword = st.text_input("Enter your keyword")
    st.form_submit_button("Search")