import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def relatorio_Dda():
    df = pd.read_excel('relatorio_integracao/Resultado.xls')

    filtro_colunas = df[(df['Status'] == 'Ativo') & (df['Pós venda'] == 'Sim') & (df['Participação DDA'] == 'Não')][['Aluno', 'Telefone Celular']]

    filtro_colunas.to_excel('listasender.xlsx', index=False)
    # Converter o DataFrame para CSV
    filtro_colunas.to_csv('listasender.csv', index=False, encoding='utf-8', sep=';')

    csv = filtro_colunas.to_csv(index=False, encoding='utf-8', sep=';')

    st.title("Integração alunos DDA")

    st.write("""
        Tabela de alunos de Pós venda, sem DDA.
    """)
    
    st.download_button(
        label="Baixar CSV",
        data=csv.encode('utf-8'),
        file_name='integracaodda.csv',
        mime='text/csv'
    )

    st.write(filtro_colunas)

def assiduidade_Interativo():
    assiduidade = pd.read_excel('./interativo/retencao/setembro.xls')
    assiduidade = assiduidade.drop(columns=['Contato Emergência 1'])
    assiduidade = assiduidade.drop(columns=['Contato Emergência 2'])
    assiduidade = assiduidade.drop(columns=['Contato Emergência 3'])
    assiduidade = assiduidade.drop(columns=['Contato Emergência 4'])
    assiduidade = assiduidade.drop(columns=['Contrato'])
    assiduidade = assiduidade.drop(columns=['Telefone Aluno'])
    assiduidade = assiduidade.drop(columns=['Data'])
    soma_multiplas_colunas = assiduidade[['Presenças', 'Faltas']].sum()
    soma_total = soma_multiplas_colunas.sum().sum()
    porcentagem_colunas = (soma_multiplas_colunas / soma_total) * 100
    ranking_frequentes = assiduidade.sort_values(by='Presenças', ascending=False)

    # Calculando a soma de Salario e Bonificacao
    ranking_frequentes['Total'] = ranking_frequentes['Presenças'] + ranking_frequentes['Faltas']

    # Calculando a porcentagem de cada Total em relação ao total geral
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

    st.write(porcentagem_colunas)
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

relatorio_Dda()

assiduidade_Interativo()