import os
import streamlit as st
import cx_Oracle
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from views.principal import show_principal
from views.agendamentos import show_agendamentos
from views.atrasados import show_atrasados
from views.acompanhamento_pagamentos import show_acompanhamento
from views.envio_obs import show_envios
from views.demandas import show_demandas


st.set_page_config(page_title='PROSIGEF', layout='wide')

menu = {
    'Página Inicial': show_principal,
    'Agendamentos': show_agendamentos,
    'Acompanhamento de OBs/PPs': show_acompanhamento,
    'Envio de Ordens Bancárias': show_envios,
    'Pagamentos Atrasados': show_atrasados,
    'Acompanhamento de Demandas': show_demandas
}

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
SERVICE_NAME = os.getenv("SERVICE_NAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

dsn = cx_Oracle.makedsn(HOST, PORT, service_name=SERVICE_NAME)
con = cx_Oracle.connect(user=USER,
                        password=PASSWORD, dsn=dsn, encoding="UTF-8")

with st.sidebar:

    st.header('PROSIGEF')

    pag_selecionada = option_menu(menu_title=None, options=list(menu.keys()))

if pag_selecionada == 'Página Inicial':
    menu[pag_selecionada]()
else:
    menu[pag_selecionada](con)
