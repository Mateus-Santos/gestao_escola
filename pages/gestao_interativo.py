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

    ranking_frequentes['Frequencia'] = ((ranking_frequentes['Presenças'] / ranking_frequentes['Total'])).apply(lambda x: f"{x:.2%}")
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

def tratamento_Modulos(material):
    entrega_Modulos()

def entrega_Modulos():
    st.title('Relatório de entrega de apostilas')
    material = pd.read_excel('database/interativo/estoque_modulos/modulos.xlsx', header=1)
    #Removendo colunas desnecessarias.
    remover_itens = ['ESTUDANTES', 'Unnamed: 26', 'Unnamed: 30', 'X', 'O', 'N']
    material = material.drop(columns=remover_itens)
    st.write(material)
    listar_modulos = [item for item in material if item not in remover_itens]
    #Realizando contagem de módulos
    nao_entregues = 'O'
    qtd_nao_entregues = material.apply(lambda col: col.value_counts().get(nao_entregues, 0))
    #Tabela de quantidade de módulos restantes.
    st.write("Relatório de módulos")
    st.write(qtd_nao_entregues)

entrega_Modulos()
assiduidade_Interativo()