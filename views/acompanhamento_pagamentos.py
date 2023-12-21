import os
import sys
import cx_Oracle
import pandas as pd
from datetime import datetime, date, timedelta
import streamlit as st


def show_acompanhamento(con):

    col_tipo, col_data, *_ = st.columns(4)

    with col_tipo:

        tipo = st.selectbox('Tipo de documento', options=[
                            'Ordem Bancária', 'Preparação de Pagamento'])

    with col_data:
        data = st.date_input(
            label="Data Inicial", format='DD/MM/YYYY')

    if tipo == 'Ordem Bancária':

        st.markdown("""
            <style>
                #MainMenu {visibility: hidden;}
                .stDeployButton {display:none;}
                footer {visibility: hidden;}
            </style>
        """, unsafe_allow_html=True)

        dsn = cx_Oracle.makedsn('10.1.0.231', 1521, service_name="sigef")
        con = cx_Oracle.connect(user="sigefconsulta",
                                password="sigefconsulta*", dsn=dsn, encoding="UTF-8")

        tab1, tab2 = st.tabs(tabs=['Conta 1000', 'Demais contas'])

        with tab1:
            query = f'''SELECT 
            unique(e.NUORDEMBANCARIA) AS OB,
            o.SGORGAO as SIGLA,
            e.VLTOTAL AS VALOR,
            cast(e.DEOBSERVACAO as varchar(50)) AS OBSERVACAO,
            e.cdsituacaoordembancaria as STATUS,
            e.dtenvio AS ENVIO,
            TO_CHAR(e.dtenvio, 'DD/MM/YYYY  -  HH:MI') as LIBERADA
            FROM SIGEF2023.EFINORDEMBANCARIA e 
            inner join SIGEF2023.EADMDOMICILIOBANCARIOUGGESTAO d ON e.NUSEQDOMICILIOUGGESTAO=d.NUSEQDOMICILIO and e.CDUNIDADEGESTORA=d.CDUNIDADEGESTORA AND e.CDGESTAO=d.CDGESTAO
            inner join SIGEF2023.eadmUNIDADEGESTORA u on e.cdunidadegestora=u.cdunidadegestora
            inner join SIGEF2023.eadmorgao o on u.cdorgao=o.cdorgao
            WHERE DTENVIO >= TO_DATE('{data}', 'YYYY-MM-DD') and e.cdsituacaoordembancaria in ('EI') and d.nuconta like '%10006'
            ORDER BY ENVIO ASC
            '''
            df = pd.read_sql(query, con)
            df['VALOR'].astype(float).round(2)

            st.dataframe(
                df,
                width=1300,
                height=700,
                column_order=['OB', 'SIGLA', 'VALOR',
                              'OBSERVACAO', 'STATUS', 'LIBERADA'],
                column_config={
                    'VALOR': st.column_config.NumberColumn(format="R$ %.2f")
                }
            )

        with tab2:
            query = f'''SELECT 
            unique(e.NUORDEMBANCARIA) AS OB,
            o.SGORGAO as SIGLA,
            e.VLTOTAL AS VALOR,
            cast(e.DEOBSERVACAO as varchar(50)) AS OBSERVACAO,
            e.cdsituacaoordembancaria as STATUS,
            e.dtenvio AS ENVIO,
            TO_CHAR(e.dtenvio, 'DD/MM/YYYY  -  HH:MI') as LIBERADA
            FROM SIGEF2023.EFINORDEMBANCARIA e 
            inner join SIGEF2023.EADMDOMICILIOBANCARIOUGGESTAO d ON e.NUSEQDOMICILIOUGGESTAO=d.NUSEQDOMICILIO and e.CDUNIDADEGESTORA=d.CDUNIDADEGESTORA AND e.CDGESTAO=d.CDGESTAO
            inner join SIGEF2023.eadmUNIDADEGESTORA u on e.cdunidadegestora=u.cdunidadegestora
            inner join SIGEF2023.eadmorgao o on u.cdorgao=o.cdorgao
            WHERE DTENVIO >= TO_DATE('{data}', 'YYYY-MM-DD') and e.cdsituacaoordembancaria in ('EI') and d.nuconta not like '%10006'
            ORDER BY ENVIO ASC
            '''
            df = pd.read_sql(query, con)
            df['VALOR'].astype(float).round(2)

            st.dataframe(
                df,
                width=1300,
                height=700,
                column_order=['OB', 'SIGLA', 'VALOR',
                              'OBSERVACAO', 'STATUS', 'LIBERADA'],
                column_config={
                    'VALOR': st.column_config.NumberColumn(format="R$ %.2f")
                }
            )

        con.close()

    if tipo == 'Preparação de Pagamento':
        st.markdown("""
            <style>
                .reportview-container {
                    margin-top: -2em;
                }
                #MainMenu {visibility: hidden;}
                .stDeployButton {display:none;}
                footer {visibility: hidden;}
            </style>
        """, unsafe_allow_html=True)

        dsn = cx_Oracle.makedsn('10.1.0.231', 1521, service_name="sigef")
        con = cx_Oracle.connect(user="sigefconsulta",
                                password="sigefconsulta*", dsn=dsn, encoding="UTF-8")

        tab1, tab2 = st.tabs(tabs=['Conta 1000', 'Demais contas'])

        with tab1:
            query = f'''
            SELECT
                pp.nupreparacaopagamento as PP,
                e.NUORDEMBANCARIA AS OB,
                o.SGORGAO as SIGLA,
                cast(pp.DEOBSERVACAO as varchar(100)) AS "OBSERVACAO da PP",
                cpp.detipocancelamentopp as STATUS,
                e.dtenvio AS ENVIO,
                TO_CHAR(e.dtenvio, 'DD/MM/YYYY  -  HH24:MI') as LIBERADA
            FROM SIGEF2023.EFINORDEMBANCARIA e 
            inner join SIGEF2023.EADMDOMICILIOBANCARIOUGGESTAO d ON e.NUSEQDOMICILIOUGGESTAO=d.NUSEQDOMICILIO and e.CDUNIDADEGESTORA=d.CDUNIDADEGESTORA AND e.CDGESTAO=d.CDGESTAO
            inner join SIGEF2023.eadmUNIDADEGESTORA u on e.cdunidadegestora=u.cdunidadegestora
            inner join SIGEF2023.eadmorgao o on u.cdorgao=o.cdorgao 
            inner join SIGEF2023.EFINPREPARACAOPAGAMENTO pp on e.nuordembancaria=pp.nuordembancaria and e.cdunidadegestora=pp.cdunidadegestora and e.cdgestao=pp.cdgestao 
            inner join SIGEF2023.EFINTIPOCANCELAMENTOPP cpp on pp.flcancelamento=cpp.cdtipocancelamentopp
            WHERE DTENVIO >= TO_DATE('{data}', 'YYYY-MM-DD') and pp.flcancelamento=0 and d.nuconta  like '%10006'
            ORDER BY ENVIO ASC
            '''
            df = pd.read_sql(query, con)

            st.dataframe(
                df,
                width=1300,
                height=700,
                column_order=['PP', 'OB', 'SIGLA', 'VALOR',
                              'OBSERVACAO da PP', 'STATUS', 'LIBERADA'],
                column_config={
                    'VALOR': st.column_config.NumberColumn(format="R$ %.2f")
                }
            )

        with tab2:
            query = f'''
            SELECT
                pp.nupreparacaopagamento as PP,
                e.NUORDEMBANCARIA AS OB,
                o.SGORGAO as SIGLA,
                cast(pp.DEOBSERVACAO as varchar(100)) AS "OBSERVACAO da PP",
                cpp.detipocancelamentopp as STATUS,
                e.dtenvio AS ENVIO,
                TO_CHAR(e.dtenvio, 'DD/MM/YYYY  -  HH24:MI') as LIBERADA
            FROM SIGEF2023.EFINORDEMBANCARIA e 
            inner join SIGEF2023.EADMDOMICILIOBANCARIOUGGESTAO d ON e.NUSEQDOMICILIOUGGESTAO=d.NUSEQDOMICILIO and e.CDUNIDADEGESTORA=d.CDUNIDADEGESTORA AND e.CDGESTAO=d.CDGESTAO
            inner join SIGEF2023.eadmUNIDADEGESTORA u on e.cdunidadegestora=u.cdunidadegestora
            inner join SIGEF2023.eadmorgao o on u.cdorgao=o.cdorgao 
            inner join SIGEF2023.EFINPREPARACAOPAGAMENTO pp on e.nuordembancaria=pp.nuordembancaria and e.cdunidadegestora=pp.cdunidadegestora and e.cdgestao=pp.cdgestao 
            inner join SIGEF2023.EFINTIPOCANCELAMENTOPP cpp on pp.flcancelamento=cpp.cdtipocancelamentopp
            WHERE DTENVIO >= TO_DATE('{data}', 'YYYY-MM-DD') and pp.flcancelamento=0 and d.nuconta not like '%10006'
            ORDER BY ENVIO ASC
            '''
            df = pd.read_sql(query, con)

            st.dataframe(
                df,
                width=1300,
                height=700,
                column_order=['PP', 'OB', 'SIGLA', 'VALOR',
                              'OBSERVACAO da PP', 'STATUS', 'LIBERADA'],
                column_config={
                    'VALOR': st.column_config.NumberColumn(format="R$ %.2f")
                }
            )

        con.close()
