import pandas as pd
import streamlit as st
from datetime import datetime
from services.services_interativo import update_database, assiduidade_Interativo, faltantes_retencao, grafico_assiduidade, exibir_vagas

#Estrutura da página
try:
    print("Tela de Gestão Interativo")
    st.title("Quadro de Vagas - Interativo")
    st.dataframe(exibir_vagas(), hide_index=True)
    st.title("Atualize a base de dados do relatório de assiduidade interativo.")
    col1, col2 = st.columns(2)
    anos = [2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
    with col1:
        mes_selecionado = st.selectbox("Selecione o mês:", ["janeiro", "fevereiro", "marco", "abril", "maio", 
                                                        "junho", "julho", "agosto", "setembro", "outubro", 
                                                        "novembro", "dezembro"], index=datetime.now().month-1)
    if datetime.now().year in anos:
        ano_atual = anos.index(datetime.now().year)
    else:
        ano_atual = None
    with col2:
        ano = st.selectbox("Selecione o ano:", anos, index=ano_atual)

    base_assiduidade_interativo = st.file_uploader("Escolha um arquivo Excel", type=['xlsx', 'xls'], key="base_assiduidade_interativo")
    local_planilha = f'./database/interativo/retencao/{ano}{mes_selecionado}.xls'
    update_database(local_planilha, base_assiduidade_interativo)

    st.title("""
                Relatório de retenção interativo.
            """)
    
    st.dataframe(assiduidade_Interativo(local_planilha), hide_index=True)

    st.title("""
            Lista dos alunos que faltaram 2 vezes ou mais:
        """)
    dados_faltantes = faltantes_retencao(local_planilha)
    st.download_button(
        label="Baixar planilha de faltantes CSV",
        data=dados_faltantes[1].encode('utf-8'),
        file_name='retencao_interativo.csv',
        mime='text/csv'
    )
    st.dataframe(dados_faltantes[0], hide_index=True)
    st.title("📊 Gráfico de Assiduidade por Mês - Interativo")
    grafico_assiduidade()

except FileNotFoundError:
    st.title("Base de dados não cadastrada, deseja realizar o cadastro?")