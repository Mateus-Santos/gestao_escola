import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
import sys
from dotenv import load_dotenv
from datetime import datetime
from main import update_database
from apis.api_quadro import local_Sheets

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
    st.dataframe(ranking_frequentes)
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

@st.cache_data(ttl=600)
def grafico_assiduidade():
    ano_inicial = 2022
    hoje = datetime.today()
    ano_atual, mes_atual = hoje.year, hoje.month
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", 
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

    dados = {"Mês": [], "Assiduidade": []}
    
    for ano in range(ano_inicial, ano_atual + 1):
        for mes_idx, mes_nome in enumerate(meses, start=1):
            if ano == ano_atual and mes_idx > mes_atual:
                break
            try:
                arquivo = pd.DataFrame(local_Sheets(f'{ano}{mes_nome}', os.getenv("ID_PLANILHA_INTERATIVO")))
                arquivo = arquivo.rename(columns={0: 'CONTRATO', 1: 'NOME', 2: 'STATUS', 3: 'TEL1', 4: 'Presenças', 5: 'Faltas', 6: 'Reposições'})
                arquivo['Presenças'] = arquivo['Presenças'].astype(int)
                arquivo['Faltas'] = arquivo['Faltas'].astype(int)
                arquivo['Total'] = arquivo['Presenças'] + arquivo['Faltas']
                presencas_mes = arquivo['Presenças'].sum()
                total_chamadas = arquivo['Total'].sum()
                assiduidade = (presencas_mes/total_chamadas) * 100
                dados["Mês"].append(f"{mes_nome}/{ano}")
                dados["Assiduidade"].append(round(assiduidade, 2))

            except Exception as e:
                print(f"Planilha não encontrada: {ano}{mes_nome}: {e}")

    df_final = pd.DataFrame(dados)

    st.write("📊 Gráfico de Assiduidade por Mês - Interativo")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_final["Mês"], df_final["Assiduidade"], marker="o", linestyle="-", color="b", label="assiduidade")

    for i, txt in enumerate(df_final["Assiduidade"]):
        ax.text(i, txt + 1, f"{txt}%", ha="center", fontsize=10, fontweight="bold", color="black")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Assiduidade (%)")
    ax.set_title("Assiduidade por Mês")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

try:
    #Estrutura da página
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

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    load_dotenv(dotenv_path)
    assiduidade_Interativo(local_planilha)
    faltantes_retencao(local_planilha)
    grafico_assiduidade()
except FileNotFoundError:
    st.title("Base de dados não cadastrada, deseja realizar o cadastro?")