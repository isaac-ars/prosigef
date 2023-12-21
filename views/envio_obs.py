import os
import sys
import pandas as pd
from datetime import datetime, date, timedelta
import streamlit as st
from io import BytesIO


def show_envios(con):

    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    col_tipo, col_data_i, col_data_f, _ = st.columns(4)

    tab1, tab2 = st.tabs(tabs=['Conta 1000', 'Demais contas'])

    with col_tipo:
        tipo = st.selectbox(label='Tipo de Análise',
                            options=['Data', 'Período'])

    if tipo == 'Data':
        with col_data_i:
            data_i = st.date_input(label="Data", format='DD/MM/YYYY')
            data_f = data_i + timedelta(1)
        with tab1:
            query1 = f'''SELECT 
                        unique(e.NUORDEMBANCARIA) AS OB,
                        o.SGORGAO as SIGLA,
                        e.VLTOTAL AS VALOR,
                        cast(e.DEOBSERVACAO as varchar(100)) AS OBSERVACAO,
                        e.cdsituacaoordembancaria as STATUS,
                        TO_CHAR(e.dtenvio, 'DD/MM/YYYY  -  HH24:MI') as LIBERADA
                    FROM SIGEF2023.EFINORDEMBANCARIA e 
                    inner join SIGEF2023.EADMDOMICILIOBANCARIOUGGESTAO d ON e.NUSEQDOMICILIOUGGESTAO=d.NUSEQDOMICILIO and e.CDUNIDADEGESTORA=d.CDUNIDADEGESTORA AND e.CDGESTAO=d.CDGESTAO
                    inner join SIGEF2023.eadmUNIDADEGESTORA u on e.cdunidadegestora=u.cdunidadegestora
                    inner join SIGEF2023.eadmorgao o on u.cdorgao=o.cdorgao
                    WHERE DTENVIO >= TO_DATE('{data_i}', 'yyyy-MM-dd') and DTENVIO < TO_DATE('{data_f}', 'yyyy-MM-dd') and e.cdsituacaoordembancaria in ('CB', 'EI', 'EN') and d.nuconta like '%10006'
                    ORDER BY e.nuordembancaria ASC'''

            df = pd.read_sql(query1, con)
            st.dataframe(df, column_config={
                'VALOR': st.column_config.NumberColumn(format="R$ %.2f"),
                'OBSERVACAO': st.column_config.Column(width="large")
            }, width=1300, height=640,
                column_order=['OB', 'SIGLA', 'VALOR', 'OBSERVACAO', 'STATUS', 'LIBERADA'])
            output = BytesIO()
            df.to_excel(output)
            st.download_button(label="Download", data=output.getvalue(),
                               file_name=f"enviadas_dia_{data_i.day}-{data_i.month}-{data_i.year}_1000.xlsx", type="primary")

        with tab2:
            query2 = f'''SELECT 
                        unique(e.NUORDEMBANCARIA) AS OB,
                        o.SGORGAO as SIGLA,
                        e.VLTOTAL AS VALOR,
                        cast(e.DEOBSERVACAO as varchar(100)) AS OBSERVACAO,
                        e.cdsituacaoordembancaria as STATUS,
                        TO_CHAR(e.dtenvio, 'DD/MM/YYYY  -  HH24:MI') as LIBERADA
                    FROM SIGEF2023.EFINORDEMBANCARIA e 
                    inner join SIGEF2023.EADMDOMICILIOBANCARIOUGGESTAO d ON e.NUSEQDOMICILIOUGGESTAO=d.NUSEQDOMICILIO and e.CDUNIDADEGESTORA=d.CDUNIDADEGESTORA AND e.CDGESTAO=d.CDGESTAO
                    inner join SIGEF2023.eadmUNIDADEGESTORA u on e.cdunidadegestora=u.cdunidadegestora
                    inner join SIGEF2023.eadmorgao o on u.cdorgao=o.cdorgao
                    WHERE DTENVIO >= TO_DATE('{data_i}', 'yyyy-MM-dd') and DTENVIO < TO_DATE('{data_f}', 'yyyy-MM-dd') and e.cdsituacaoordembancaria in ('CB', 'EI', 'EN') and d.nuconta not like '%10006'
                    ORDER BY e.nuordembancaria ASC'''

            df = pd.read_sql(query2, con)
            st.dataframe(df, column_config={
                'VALOR': st.column_config.NumberColumn(format="R$ %.2f"),
                'OBSERVACAO': st.column_config.Column(width="large")
            }, width=1300, height=640,
                column_order=['OB', 'SIGLA', 'VALOR', 'OBSERVACAO', 'STATUS', 'LIBERADA'])
            output = BytesIO()
            df.to_excel(output)
            st.download_button(label="Download", data=output.getvalue(),
                               file_name=f"enviadas_dia_{data_i.day}-{data_i.month}-{data_i.year}.xlsx", type="primary")

    if tipo == 'Período':
        with col_data_i:
            data_i = st.date_input(
                label="Data Inicial", format='DD/MM/YYYY')

        with col_data_f:
            data_f = st.date_input(label="Data Final", format='DD/MM/YYYY')

        with tab1:
            query1 = f'''SELECT 
                        unique(e.NUORDEMBANCARIA) AS OB,
                        o.SGORGAO as SIGLA,
                        e.VLTOTAL AS VALOR,
                        cast(e.DEOBSERVACAO as varchar(100)) AS OBSERVACAO,
                        e.cdsituacaoordembancaria as STATUS,
                        e.dtenvio AS ENVIO,
                        TO_CHAR(e.dtenvio, 'DD/MM/YYYY  -  HH24:MI') as LIBERADA
                    FROM SIGEF2023.EFINORDEMBANCARIA e 
                    inner join SIGEF2023.EADMDOMICILIOBANCARIOUGGESTAO d ON e.NUSEQDOMICILIOUGGESTAO=d.NUSEQDOMICILIO and e.CDUNIDADEGESTORA=d.CDUNIDADEGESTORA AND e.CDGESTAO=d.CDGESTAO
                    inner join SIGEF2023.eadmUNIDADEGESTORA u on e.cdunidadegestora=u.cdunidadegestora
                    inner join SIGEF2023.eadmorgao o on u.cdorgao=o.cdorgao
                    WHERE DTENVIO >= TO_DATE('{data_i}', 'yyyy-MM-dd') and DTENVIO < TO_DATE('{data_f + timedelta(1)}', 'yyyy-MM-dd') and e.cdsituacaoordembancaria in ('CB', 'EI', 'EN') and d.nuconta like '%10006'
                    ORDER BY ENVIO ASC'''

            df = pd.read_sql(query1, con)
            st.dataframe(df, column_config={
                'VALOR': st.column_config.NumberColumn(format="R$ %.2f"),
                'OBSERVACAO': st.column_config.Column(width="large")
            }, width=1300, height=640,
                column_order=['OB', 'SIGLA', 'VALOR', 'OBSERVACAO', 'STATUS', 'LIBERADA'])
            output = BytesIO()
            df.to_excel(output)
            print(data_i)
            st.download_button(label="Download", data=output.getvalue(),
                               file_name=f"enviadas_dia_{data_i.month}-{data_i.year}_1000.xlsx", type="primary")

        with tab2:
            query2 = f'''SELECT 
                        unique(e.NUORDEMBANCARIA) AS OB,
                        o.SGORGAO as SIGLA,
                        e.VLTOTAL AS VALOR,
                        cast(e.DEOBSERVACAO as varchar(100)) AS OBSERVACAO,
                        e.cdsituacaoordembancaria as STATUS,
                        e.dtenvio AS ENVIO,
                        TO_CHAR(e.dtenvio, 'DD/MM/YYYY  -  HH24:MI') as LIBERADA
                    FROM SIGEF2023.EFINORDEMBANCARIA e 
                    inner join SIGEF2023.EADMDOMICILIOBANCARIOUGGESTAO d ON e.NUSEQDOMICILIOUGGESTAO=d.NUSEQDOMICILIO and e.CDUNIDADEGESTORA=d.CDUNIDADEGESTORA AND e.CDGESTAO=d.CDGESTAO
                    inner join SIGEF2023.eadmUNIDADEGESTORA u on e.cdunidadegestora=u.cdunidadegestora
                    inner join SIGEF2023.eadmorgao o on u.cdorgao=o.cdorgao
                    WHERE DTENVIO >= TO_DATE('{data_i}', 'yyyy-MM-dd') and DTENVIO < TO_DATE('{data_f + timedelta(1)}', 'yyyy-MM-dd') and e.cdsituacaoordembancaria in ('CB', 'EI', 'EN') and d.nuconta not like '%10006'
                    ORDER BY ENVIO ASC'''

            df = pd.read_sql(query2, con)
            st.dataframe(df, column_config={
                'VALOR': st.column_config.NumberColumn(format="R$ %.2f"),
                'OBSERVACAO': st.column_config.Column(width="large")
            }, width=1300, height=640,
                column_order=['OB', 'SIGLA', 'VALOR',
                              'OBSERVACAO', 'STATUS', 'LIBERADA']
            )
            output = BytesIO()
            df.to_excel(output)
            st.download_button(label="Download", data=output.getvalue(),
                               file_name=f"enviadas_dia_{data_i.month}-{data_i.year}.xlsx", type="primary")

    con.close()
