import streamlit as st
import locale
import pandas as pd


def show_agendamentos(con):

    locale.setlocale(locale.LC_ALL, '')

    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    col_d, *_ = st.columns(3)

    tab1, tab2 = st.tabs(tabs=['Log de Agendamentos', 'Execução de Tarefas'])

    with col_d:
        data = st.date_input(label="Data Inicial", format='DD/MM/YYYY')

    with tab1:
        col1, col2 = st.columns(2)
        query1 = f'''
        select
            cast(agd.cdlog as varchar(10)) as CODIGO,
            agm.nmagendamento as AGENDAMENTO,
            agd.delogerro as MENSAGEM,
            agd.destacktrace,
            TO_CHAR(agd.dtultalteracao, 'DD/MM/YYYY  -  HH24:MI') as DATA_HORA
        from sigef.eadmlogagendador agd
        inner join sigef.eadmagendamento agm
            on agd.cdagendamento=agm.cdagendamento
        where agd.dtultalteracao >= to_date('{data}', 'YYYY-MM-DD') 
        order by agd.dtultalteracao desc
        '''

        df = pd.read_sql(query1, con, index_col='CODIGO')
        opcoes = df['AGENDAMENTO'].sort_values(ascending=True)
        with col1:
            agendamentos = st.multiselect(
                label='Filtrar por agendamentos', options=opcoes.unique())

        if agendamentos:
            st.dataframe(df[df['AGENDAMENTO'].isin(agendamentos)], height=600,
                         width=1300)
        else:
            st.dataframe(df, height=600, width=1300)

    with tab2:

        col1, col2 = st.columns(2)

        query2 = f'''
        SELECT
            cast(t.cdtarefa as varchar(15)) as CODIGO, 
            a.NMAGENDAMENTO AS AGENDAMENTO,
            s.desituacaotarefa AS STATUS,
            TO_CHAR(t.DTINICIO, 'DD/MM/YYYY  -  HH24:MI') AS PREVISTA,
            TO_CHAR(t.DTINICIOREAL, 'DD/MM/YYYY  -  HH24:MI') AS INICIADA,
            TO_CHAR(t.DTTERMINOREAL, 'DD/MM/YYYY  -  HH24:MI') AS CONCLUIDA	
        FROM SIGEF.EADMTAREFA t
        INNER JOIN SIGEF.EADMAGENDAMENTO a ON t.CDAGENDAMENTO=a.CDAGENDAMENTO 
        INNER JOIN SIGEF.EADMSITUACAOTAREFA s ON t.CDSITUACAOTAREFA=s.CDSITUACAOTAREFA 
        WHERE t.DTINICIO >= TO_DATE('{data}', 'YYYY-MM-DD')
        ORDER BY T.DTINICIO DESC 
        '''
        df2 = pd.read_sql(query2, con, index_col='CODIGO')
        opcoes2 = df2['AGENDAMENTO'].sort_values(ascending=True)
        opcoes3 = df2['STATUS'].sort_values(ascending=True)
        with col1:
            agendamentos2 = st.multiselect(
                label='Filtrar de tarefas', options=opcoes2.unique())
        if agendamentos2:
            st.dataframe(df2[df2['AGENDAMENTO'].isin(
                agendamentos2)], height=600, width=1300)
        else:
            st.dataframe(df2, width=1300, height=600)

    con.close()
