import pandas as pd
import streamlit as st
import os
import matplotlib.pyplot as plt
from datetime import datetime

# Mensagem Principal.
st.title("Bem-vindo a tela de relatórios do Instituto Mix.")
st.write("Aqui você poderá acompanhar toda a situação atualizada que ocorre nos setores da escola.")

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
        arquivo = f"./database/bases de dados/{ano}/{ano}{mes_nome}.xls"
        try:
            df = pd.read_excel(arquivo)
            ranking_frequentes = df.sort_values(by='Presenças', ascending=False)
            ranking_frequentes['Total'] = ranking_frequentes['Presenças'] + ranking_frequentes['Faltas']
            presencas_mes = ranking_frequentes['Presenças'].sum()
            total_chamadas = ranking_frequentes['Total'].sum()
            assiduidade = (presencas_mes/total_chamadas) * 100
            dados["Mês"].append(f"{mes_nome}/{ano}")
            dados["Assiduidade"].append(round(assiduidade, 2))

        except FileNotFoundError:
            print(f"Arquivo {arquivo} não encontrado. Pulando...")

df_final = pd.DataFrame(dados)

st.title("📊 Gráfico de Assiduidade por Mês")

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