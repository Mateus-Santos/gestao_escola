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