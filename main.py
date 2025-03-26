import pandas as pd
import streamlit as st
import os
import matplotlib.pyplot as plt
from datetime import datetime
from apis.api_quadro import local_Sheets
from dotenv import load_dotenv

# Mensagem Principal.
st.title("Bem-vindo a tela de relatórios do Instituto Mix.")
st.write("Aqui você poderá acompanhar toda a situação atualizada que ocorre nos setores da escola.")

ano_inicial = 2022
hoje = datetime.today()
ano_atual, mes_atual = hoje.year, hoje.month
meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", 
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

dados = {"Mês": [], "Assiduidade": []}
load_dotenv()

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

def update_database(caminho_arquivo, uploaded_file):
    # Mensagem para atualizar a base de dados integração DDA.
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)
        with open(caminho_arquivo, "wb") as file:
            file.write(uploaded_file.getbuffer())
        st.success(f"O arquivo foi substituído com sucesso em {caminho_arquivo}")