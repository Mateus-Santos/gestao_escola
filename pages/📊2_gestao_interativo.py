import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime

from main import update_database

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def assiduidade_Interativo(local_planilha):
    assiduidade = pd.read_excel(local_planilha)
    assiduidade = assiduidade.drop(columns=['Contato Emergência 1', 'Contato Emergência 2', 
                                            'Contato Emergência 3', 'Contato Emergência 4', 
                                            'Contrato', 'Telefone Aluno', 'Data', 'Reposições', 'Status'])
    ranking_frequentes = assiduidade.sort_values(by='Presenças', ascending=False)
    ranking_frequentes['Total'] = ranking_frequentes['Presenças'] + ranking_frequentes['Faltas']
    ranking_frequentes['Frequencia'] = (ranking_frequentes['Presenças'] / ranking_frequentes['Total']) * 100
    ranking_frequentes['Frequencia'] = ranking_frequentes['Frequencia'].replace(['inf%', '-inf%'], '0%')
    ranking_frequentes = ranking_frequentes.sort_values(by='Frequencia', ascending=False)
    st.title("""
            Relatório de retenção interativo.
        """)
    presenca = ranking_frequentes['Presenças'].sum()
    falta = ranking_frequentes['Faltas'].sum()
    dados_pizza = {
    'Presença': presenca,
    'Falta': falta,
    }
    cores = ['#00FF00','#FF0000']
    # Criar o gráfico de pizza
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.pie(dados_pizza.values(), labels=dados_pizza.keys(), 
        autopct='%1.1f%%', 
        startangle=70, 
        colors=cores, textprops={'fontsize': 7})
    ax.set_title('Distribuição de Presenças e Faltas', fontsize=12)
    fig.patch.set_facecolor('white')
    st.pyplot(fig)
    st.title("""
            Ranking alunos mais frequentes interativo.
        """)
    st.dataframe(ranking_frequentes, hide_index=True)
    

def faltantes_retencao(local_arquivo):
    assiduidade = pd.read_excel(local_arquivo)
    assiduidade = assiduidade.drop(columns=['Contato Emergência 1', 'Contato Emergência 2', 
                                            'Contato Emergência 3', 'Contato Emergência 4', 
                                            'Contrato', 'Data', 'Reposições', 'Presenças'])
    faltantes = assiduidade[['Nome Aluno']]
    faltantes = assiduidade[(assiduidade['Status'] == 'Ativo') & (assiduidade['Faltas'] >= 2)]
    faltantes = faltantes.drop(columns=['Status'])
    st.title("""
            Lista dos alunos que mais faltaram:
        """)
    csv = faltantes.to_csv(index=False, encoding='utf-8', sep=';')
    st.download_button(
        label="Baixar planilha de faltantes CSV",
        data=csv.encode('utf-8'),
        file_name='retencao_interativo.csv',
        mime='text/csv'
    )
    st.dataframe(faltantes, hide_index=True)

st.title("Atualize a base de dados do relatório de assiduidade interativo.")

col1, col2 = st.columns(2)
anos = [2021, 2022, 2023, 2024, 2025, 2026, 2027]

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

try:
    assiduidade_Interativo(local_planilha)
    faltantes_retencao(local_planilha)
except FileNotFoundError:
    st.title("Base de dados não cadastrada, deseja realizar o cadastro?")