import base64
import streamlit as st
from fairmofapp.analyzer import similarity_graph
from fairmofapp.analyzer.adj_matrix_loader import get_adjacency_matrix



st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<h1 class="centered-title">Welcome to FAIRMOF App Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="centered-title">An efficient tool to accerate the discovery of MOFs</h3>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


mof_name = st.text_input("Enter MOF name (e.g., ABAFUH):")
top_n = st.slider("How many similar MOFs to display?", min_value=1, max_value=100, value=5)
