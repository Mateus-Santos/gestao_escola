import pandas as pd
import streamlit as st
import os

# Mensagem Principal.
st.title("Bem-vindo a tela de relatórios do Instituto Mix.")
st.write("Aqui você poderá acompanhar toda a situação atualizada que ocorre nos setores da escola.")

def update_database(caminho_arquivo, uploaded_file):
    # Mensagem para atualizar a base de dados integração DDA.
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)
        with open(caminho_arquivo, "wb") as file:
            file.write(uploaded_file.getbuffer())
        st.success(f"O arquivo foi substituído com sucesso em {caminho_arquivo}")

# Mensagem para atualizar a base de dados integração DDA.
st.title("Atualize a base de dados do relatório de integração DDA.")
base_relatorio_dda = st.file_uploader("Escolha um arquivo Excel", type=['xlsx', 'xls'], key="base_relatorio_dda")
update_database('./database/modular/relatorio_integracao/Resultado.xls', base_relatorio_dda)

st.title("Atualize a base de dados do relatório de assiduidade interativo.")
base_assiduidade_interativo = st.file_uploader("Escolha um arquivo Excel", type=['xlsx', 'xls'], key="base_assiduidade_interativo")
update_database('./database/interativo/retencao/setembro.xls', base_assiduidade_interativo)