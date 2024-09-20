import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
import sys

from main import update_database

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def assiduidade_Interativo():
    assiduidade = pd.read_excel('database/interativo/retencao/setembro.xls')
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
    
    st.write(ranking_frequentes)

st.title("Atualize a base de dados do relatório de assiduidade interativo.")
base_assiduidade_interativo = st.file_uploader("Escolha um arquivo Excel", type=['xlsx', 'xls'], key="base_assiduidade_interativo")
update_database('./database/interativo/retencao/setembro.xls', base_assiduidade_interativo)
assiduidade_Interativo()