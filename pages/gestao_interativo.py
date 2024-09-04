import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def assiduidade_Interativo():
    assiduidade = pd.read_excel('database/interativo/retencao/setembro.xls')
    assiduidade = assiduidade.drop(columns=['Contato Emergência 1', 'Contato Emergência 2', 
                                            'Contato Emergência 3', 'Contato Emergência 4', 
                                            'Contrato', 'Telefone Aluno', 'Data', 'Reposições', 'Status'])
    ranking_frequentes = assiduidade.sort_values(by='Presenças', ascending=False)

    ranking_frequentes['Total'] = ranking_frequentes['Presenças'] + ranking_frequentes['Faltas']

    ranking_frequentes['Frequencia'] = ((ranking_frequentes['Total'] / ranking_frequentes['Presenças'])).apply(lambda x: f"{x:.2%}")
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
    material = pd.read_excel('database/interativo/estoque_modulos/modulos.xlsx', header=1)
    st.write(material)
    modulos = list(material.columns)
    modulos.remove('ESTUDANTES') 
    modulo = st.selectbox("Selecione o Módulo", modulos)
    nao_analisados = material[modulo].isnull().sum()
    st.write("Módulos Não Analisados: ", nao_analisados)
    st.subheader("Atualizar Status dos Estudantes Não Analisados: ")
    filtro = material[modulo].isnull()
    st.write(material[filtro][['ESTUDANTES', modulo]])

entrega_Modulos()
assiduidade_Interativo()
