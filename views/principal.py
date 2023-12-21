import streamlit as st


def show_principal():
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    st.title('PROSIGEF')

    st.subheader(
        'Sistema auxiliar para acompanhamento técnico e financeiro do Projeto SIGEF')
