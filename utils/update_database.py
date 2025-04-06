import os
import pandas as pd
import streamlit as st

# Essa função adiciona todos os arquivos ao local no projeto caso seja necessário.
def update_database(caminho_arquivo, uploaded_file):
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)
        with open(caminho_arquivo, "wb") as file:
            file.write(uploaded_file.getbuffer())
        print("Aquivo na base de dados atualizado com sucesso!")
        st.success(f"O arquivo foi substituído com sucesso em {caminho_arquivo}")