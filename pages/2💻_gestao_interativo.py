import pandas as pd
import streamlit as st
from datetime import datetime
from services.services_interativo import update_database, gerar_relatorio_assiduidade, listar_faltantes_retencao, plotar_grafico_assiduidade, exibir_vagas

def carregar_vagas():
    st.title("Quadro de Vagas - Interativo")
    st.dataframe(exibir_vagas(), hide_index=True)

#Estrutura da página
def main():
    print("Tela de Gestão Interativo")
    carregar_vagas()
    st.title("Atualize a base de dados do relatório de assiduidade interativo.")
    col1, col2 = st.columns(2)
    anos = list(range(2021, datetime.now().year+1))
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
    if base_assiduidade_interativo:
        update_database(local_planilha, base_assiduidade_interativo)

    st.title("""Relatório de retenção interativo:""")
    st.dataframe(gerar_relatorio_assiduidade(local_planilha), hide_index=True)
    st.title("""
            Lista dos alunos que faltaram 2 vezes ou mais:
        """)
    dados_faltantes = listar_faltantes_retencao(local_planilha)
    st.download_button(
        label="Baixar planilha de faltantes CSV",
        data=dados_faltantes[1].encode('utf-8'),
        file_name='retencao_interativo.csv',
        mime='text/csv'
    )
    st.dataframe(dados_faltantes[0], hide_index=True)
    st.title("📊 Gráfico de Assiduidade por Mês - Interativo")
    plotar_grafico_assiduidade()

try:
    main()
except FileNotFoundError:
    st.title("Base de dados não cadastrada. Deseja realizar o cadastro?")