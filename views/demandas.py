import streamlit as st
import pandas as pd
from datetime import date, datetime


def marcar_atraso(valor):
    color = '#52c87b' if valor <= 10 else '#f98074'
    return f'background-color: {color}'


def show_demandas(con):

    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    col1, col2, *_ = st.columns(5)
    with col1:
        demanda = st.text_input(label='Demanda')
    with col2:
        ano = st.selectbox(label='Início da pesquisa', options=[
                           ano for ano in range(int(date.today().year), 2016, -1)])

    try:
        tab1, tab2 = st.tabs(['Demandas', 'Detalhamento'])
        if demanda:
            query = f'''
            SELECT 
                cast(d.CDDEMANDA as varchar(10))AS DEMANDA,
                e.deencam AS "SITUAÇÃO",
                p.nmprior AS PRIORIDADE,
                d.DTINCLUSAO AS "INCLUSÃO",
                e.DTULTALTERACAO AS "ATUALIZAÇÃO",
                sysdate as DIA
            FROM SIGEF.EDEMDEMANDA d
            INNER JOIN SIGEF.EDEMENCAMINHAMENTO e ON d.CDDEMANDA = e.CDDEMANDA
            INNER JOIN SIGEF.EDEMPRIORIDADE p ON d.CDPRIOR = p.cdprior
            WHERE d.DTINCLUSAO >= TO_DATE('{ano}-01-01','YYYY-MM-DD' ) and d.CDDEMANDA ='{demanda}'
            ORDER BY d.CDDEMANDA DESC
            '''
        else:
            query = f'''
                SELECT 
                    cast(d.CDDEMANDA as varchar(10))AS DEMANDA,
                    e.deencam AS "SITUAÇÃO",
                    p.nmprior AS PRIORIDADE,
                    d.DTINCLUSAO AS "INCLUSÃO",
                    e.DTULTALTERACAO AS "ATUALIZAÇÃO",
                    sysdate as DIA
                FROM SIGEF.EDEMDEMANDA d
                INNER JOIN SIGEF.EDEMENCAMINHAMENTO e ON d.CDDEMANDA = e.CDDEMANDA
                INNER JOIN SIGEF.EDEMPRIORIDADE p ON d.CDPRIOR = p.cdprior
                WHERE d.DTINCLUSAO >= TO_DATE('{ano}-01-01','YYYY-MM-DD' ) 
                ORDER BY d.CDDEMANDA DESC
                '''
        with tab1:
            df = pd.read_sql(query, con)
            df['SITUAÇÃO'] = df['SITUAÇÃO'].astype('category')
            df['TEMPO DE RESPOSTA'] = (df['ATUALIZAÇÃO'].dt.floor('d') -
                                       df['INCLUSÃO'].dt.floor('d')).dt.days
            df.sort_values(by=['DEMANDA', 'ATUALIZAÇÃO'],
                           inplace=True, ascending=False)
            situacoes = ['Solicitado Indra', 'Em Espera', 'Codificação',
                         'Solicitato SIGEF-RN', 'Triagem', 'Solicitado SIGEF-RN']
            df['ATRASO DE ENTREGA'] = ((df['DIA'].dt.floor('d') - df['INCLUSÃO'].dt.floor('d')
                                        ).dt.days).where(df['SITUAÇÃO'].isin(situacoes), 0)

            st.dataframe(df.style.applymap(marcar_atraso, subset=['ATRASO DE ENTREGA']), column_order=['DEMANDA', 'SITUAÇÃO', 'INCLUSÃO',
                                                                                                       'TEMPO DE RESPOSTA', 'ATUALIZAÇÃO', 'ATRASO DE ENTREGA'], height=600, width=1300)
        with tab2:
            if not demanda:
                st.warning(
                    'Não foi informado o número da demanda para detalhamento')
            else:
                query_detalhe = f'''
                    SELECT 
                        cast(dem.CDDEMANDA as varchar(10))AS DEMANDA,
                        TO_CHAR(dem.DTINCLUSAO, 'DD/MM/YYYY') AS "INCLUSÃO",
                        rec.NMRECURSO AS REQUERENTE,
                        dem.SGMODULO AS MODULO,
                        dem.NMFUNCAO AS FUNCIONALIDADE,
                        ass.NMASSUNTO AS ASSUNTO,
                        pri.NMPRIOR AS PRIORIDADE,
                        sit.NMSITUACAO AS "SITUAÇÃO",
                        tde.NMTPDEM AS "TIPO PROPOSTO",
                        dem.DEDEMANDA AS "DESCRIÇÃO"
                    FROM SIGEF.EDEMDEMANDA dem
                    INNER JOIN SIGEF.EDEMENCAMINHAMENTO enc ON dem.CDDEMANDA = enc.CDDEMANDA 
                    INNER JOIN SIGEF.EDEMSITUACAO sit ON dem.CDSITUACAO = sit.CDSITUACAO 
                    INNER JOIN SIGEF.EDEMPRIORIDADE pri ON dem.CDPRIOR = pri.CDPRIOR 
                    INNER JOIN SIGEF.EDEMASSUNTO ass ON dem.CDASSUNTO = ass.CDASSUNTO 
                    INNER JOIN SIGEF.EDEMTIPODEMANDA tde ON dem.CDTPDEMPROPOSTO = tde.CDTPDEM 
                    INNER JOIN SIGEF.EDEMRECURSO rec ON dem.CDRECURSO = rec.CDRECURSO
                    WHERE dem.CDDEMANDA = {demanda} 
                    AND enc.DTULTALTERACAO = (SELECT MAX(enc.DTULTALTERACAO) FROM SIGEF.EDEMENCAMINHAMENTO enc WHERE enc.CDDEMANDA = {demanda})
                '''

                df2 = pd.read_sql(query_detalhe, con)
                # st.dataframe(df2)
                _demanda = df2.loc[0][0]
                inclusao = df2.loc[0][1]
                requerente = df2.loc[0][2]
                modulo = df2.loc[0][3]
                funcionalidade = df2.loc[0][4]
                assunto = df2.loc[0][5]
                prioridade = df2.loc[0][6]
                situacao = df2.loc[0][7]
                tipo_proposto = df2.loc[0][8]
                descricao = df2.loc[0][9]

                st.metric('DEMANDA', value=_demanda)

                st.divider()

                d1, d2 = st.columns(2)

                with d1:
                    with st.container():
                        st.markdown("###### INCLUSÃO", unsafe_allow_html=True)
                        st.text(inclusao)

                        st.markdown("###### REQUERENTE",
                                    unsafe_allow_html=True)
                        st.text(requerente)

                        st.markdown("###### MÓDULO", unsafe_allow_html=True)
                        st.text(modulo)

                        st.markdown("###### FUNCIONALIDADE",
                                    unsafe_allow_html=True)
                        st.text(funcionalidade)

                with d2:
                    with st.container():

                        st.markdown("###### ASSUNTO", unsafe_allow_html=True)
                        st.text(assunto)

                        st.markdown("###### PRIORIDADE",
                                    unsafe_allow_html=True)
                        st.text(prioridade)

                        st.markdown("###### SITUAÇÃO", unsafe_allow_html=True)
                        st.text(situacao)

                        st.markdown("###### TIPO PROPOSTO",
                                    unsafe_allow_html=True)
                        st.text(tipo_proposto)

                with st.container():
                    st.divider()
                    st.markdown("###### DESCRIÇÃO", unsafe_allow_html=True)
                    st.markdown(f'''
                    {descricao}
                    ''', unsafe_allow_html=True)

    except Exception as e:
        st.write(e)

    con.close()
