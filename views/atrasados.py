import os
import sys
import pandas as pd
from datetime import datetime, date, timedelta
import streamlit as st
from io import BytesIO


def show_atrasados(con):

    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        tabs=['Veículos', 'Imóveis PF', 'Imóveis PJ', 'Terceirizadas'])

    with tab1:
        st.subheader('Relatório de veículos')
        query1 = '''select 
            cast(P.cdunidadegestora as varchar(6)) as UG,
            cast(P.cdgestao as varchar(5)) as Gestao,
            P.nuordembancaria as OB,
            O.deobservacao as "OBSERVAÇÃO",
            C.nmcredor as CREDOR,
            C.NUCNPJ AS CNPJ,
            SUM(P.vlpreparacaopagamento) as "VALOR TOTAL"
        from 
            SIGEF2023.efinpreparacaopagamento P
        inner join 
            SIGEF2023.efinordembancaria O
        on 
            P.nuordembancaria=O.nuordembancaria
        inner join 
            SIGEF.eadmcredor C
        on 
            P.cdcredor=C.cdcredor
        where 
            O.cdsituacaoordembancaria='AO' and C.nucnpj in (03446400000113,02909308000180,05340639000130,03446400000113,27595780000116,02491558000142,03105598000171,07212081000132,11075071000170,04819323000162,03527573000166,03867672000197,10852157000107,02737691000136,05340639000130)
        group by 
            P.cdunidadegestora, 
            P.cdgestao, 
            P.nuordembancaria,
            O.deobservacao, 
            C.nmcredor, 
            C.NUCNPJ
        '''
        df = pd.read_sql(query1, con)
        df['VALOR TOTAL'].astype(float).round(2)
        st.dataframe(df, column_config={
            'VALOR TOTAL': st.column_config.NumberColumn(format="R$ %.2f")
        }, height=600)
        output = BytesIO()
        df.to_excel(output)
        st.download_button(label="Download", data=output.getvalue(),
                           file_name="relatorio_veiculos.xlsx", type="primary")

    with tab2:
        st.subheader('Relatório de Iméveis Pessoa Física')
        query3 = '''select 
            cast(P.cdunidadegestora as varchar(6)) as UG,
            cast(P.cdgestao as varchar(5)) as Gestao,
            P.nuordembancaria as OB,
            O.deobservacao as "OBSERVAÇÃO",
            C.nmcredor as CREDOR,
            C.NUCPF AS CPF,
            SUM(P.vlpreparacaopagamento) as "VALOR TOTAL"
        from 
            SIGEF2023.efinpreparacaopagamento P
        inner join 
            SIGEF2023.efinordembancaria O
        on 
            P.nuordembancaria=O.nuordembancaria
        inner join 
            SIGEF.eadmcredor C
        on 
            P.cdcredor=C.cdcredor
        where 
            O.cdsituacaoordembancaria='AO' and c.nucpf in (33629170463,87535130453,13135384420,03931714420,42966817453,47396555434,05731494452,15465004487,96778920459,24315486434)
        group by 
            P.cdunidadegestora, 
            P.cdgestao, 
            P.nuordembancaria,
            O.deobservacao, 
            C.nmcredor, 
            C.NUCPF
        '''
        df = pd.read_sql(query3, con)
        df['VALOR TOTAL'].astype(float).round(2)
        st.dataframe(df, column_config={
            'VALOR TOTAL': st.column_config.NumberColumn(format="R$ %.2f")
        }, height=600)
        output = BytesIO()
        df.to_excel(output)
        st.download_button(label="Download", data=output.getvalue(),
                           file_name="relatorio_imoveis_pf.xlsx", type="primary")

    with tab3:
        st.subheader('Relatório de Imóveis Pessoa Jurídica')
        query2 = '''select 
            cast(P.cdunidadegestora as varchar(6)) as UG,
            cast(P.cdgestao as varchar(5)) as Gestao,
            P.nuordembancaria as OB,
            O.deobservacao as "OBSERVAÇÃO",
            C.nmcredor as CREDOR,
            C.NUCNPJ AS CNPJ,
            SUM(P.vlpreparacaopagamento) as "VALOR TOTAL"
        from 
            SIGEF2023.efinpreparacaopagamento P
        inner join 
            SIGEF2023.efinordembancaria O
        on 
            P.nuordembancaria=O.nuordembancaria
        inner join 
            SIGEF.eadmcredor C
        on 
            P.cdcredor=C.cdcredor
        where 
            O.cdsituacaoordembancaria='AO' and C.nucnpj in (29463446000134,03818893000175,35660869000147,11822092000101,23800869000116,17298641000177,10537433000134,19658382000173,26437930000109,08340515000304)
        group by 
            P.cdunidadegestora, 
            P.cdgestao, 
            P.nuordembancaria,
            O.deobservacao, 
            C.nmcredor, 
            C.NUCNPJ
        '''
        df = pd.read_sql(query2, con)
        df['VALOR TOTAL'].astype(float).round(2)
        st.dataframe(df, column_config={
            'VALOR TOTAL': st.column_config.NumberColumn(format="R$ %.2f")
        }, height=600)
        output = BytesIO()
        df.to_excel(output)
        st.download_button(label="Download", data=output.getvalue(),
                           file_name="relatorio_imoveis_pj.xlsx", type="primary")

    with tab4:
        st.subheader('Relatório de Terceirizadas')
        query4 = '''select 
            cast(P.cdunidadegestora as varchar(6)) as UG,
            cast(P.cdgestao as varchar(5)) as Gestao,
            P.nuordembancaria as OB,
            O.deobservacao as "OBSERVAÇÃO",
            C.nmcredor as CREDOR,
            C.NUCNPJ AS CNPJ,
            SUM(P.vlpreparacaopagamento) as "VALOR TOTAL"
        from 
            SIGEF2023.efinpreparacaopagamento P
        inner join 
            SIGEF2023.efinordembancaria O
        on 
            P.nuordembancaria=O.nuordembancaria
        inner join 
            SIGEF.eadmcredor C
        on 
            P.cdcredor=C.cdcredor
        where 
            O.cdsituacaoordembancaria='AO' and C.nucnpj in (08220864000120,13491432000194,17679352000118,04791213000130,35519164000170,41249921000170,07387503000100,13409775000167,08220864000120,34028316002580,02567270000104,04482256000133,07442731000136)
        group by 
            P.cdunidadegestora, 
            P.cdgestao, 
            P.nuordembancaria,
            O.deobservacao, 
            C.nmcredor, 
            C.NUCNPJ
        '''
        df = pd.read_sql(query4, con)
        df['VALOR TOTAL'].astype(float).round(2)
        st.dataframe(df, column_config={
            'VALOR TOTAL': st.column_config.NumberColumn(format="R$ %.2f")
        }, height=600)
        output = BytesIO()
        df.to_excel(output)
        st.download_button(label="Download", data=output.getvalue(),
                           file_name="relatorio_terceirizadas.xlsx", type="primary")

    con.close()
