import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
import sys
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from apis.api_modulos import local_Sheets_Modulos

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

def entrega_Modulos():
    st.title('Relatório de entrega de apostilas')
    gsheets = local_Sheets_Modulos()
    colunas = gsheets[0]
    material = pd.DataFrame(data=gsheets, columns=colunas)
    material = material[1:].reset_index(drop=True)
    qtd_nao_entregues = material.apply(lambda col: col.value_counts().get('O', 0))
    excel_buffer = io.BytesIO()
    material.to_excel(excel_buffer, index=False, engine='xlsxwriter')
    excel_buffer.seek(0)
    st.download_button(
        label="Baixar Lista Completa",
        data=excel_buffer,
        file_name='Lista de Modulos.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        key='material'
    )
    excel_buffer.truncate(0)
    excel_buffer.seek(0)
    st.dataframe(material)
    qtd_nao_entregues.to_excel(excel_buffer, index=True, engine='xlsxwriter')
    excel_buffer.seek(0)
    st.write('Lista com a quantidade de Módulos para solicitar')
    st.download_button(
        label="Baixar Relatório de Módulos",
        data=excel_buffer,
        file_name='Relatorio_de_Modulos_a_Entregar.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        key='qtd_nao_entregues'
    )
    st.dataframe(qtd_nao_entregues)

def news_alunos(novos_alunos):
    if novos_alunos is not None:
        novos_alunos_df = pd.read_excel(novos_alunos)
        gsheets = local_Sheets_Modulos()
        colunas = gsheets[0]
        material = pd.DataFrame(data=gsheets, columns=colunas)
        material = material[1:].reset_index(drop=True)
        filtro = ~novos_alunos_df['Aluno'].isin(material['ESTUDANTES'])
        valores_nao_encontrados = novos_alunos_df['Aluno'][filtro]
        return st.write(valores_nao_encontrados)

entrega_Modulos()
assiduidade_Interativo()
st.title("Insira novos alunos para a analise:")
novos_alunos = st.file_uploader("Escolha um arquivo Excel", type=['xlsx', 'xls'], key="novos_alunos")
news_alunos(novos_alunos)