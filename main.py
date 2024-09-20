import pandas as pd
import streamlit as st
import os
from apis.api_modulos import update_modulos
from apis.api_modulos import local_Sheets_Modulos

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

def news_alunos(novos_alunos):
    if novos_alunos is not None:
        novos_alunos_df = pd.read_excel(novos_alunos)
        gsheets = local_Sheets_Modulos()
        #Corrigindo colunas do gsheets;
        colunas = gsheets[0]
        material = pd.DataFrame(data=gsheets, columns=colunas)
        material = material[1:].reset_index(drop=True)
        #Filtro invertido
        filtro = ~novos_alunos_df['Aluno'].isin(material['ESTUDANTES'])
        valores_nao_encontrados = novos_alunos_df['Aluno'][filtro]
        # Criar um novo DataFrame com valores não encontrados para adicionar ao final de df1
        new_material = pd.DataFrame({'ESTUDANTES': valores_nao_encontrados})
        # Adicionar os valores não encontrados ao final de 'coluna1' de df1
        material = pd.concat([material, new_material], ignore_index=True)
        material = material.fillna('A')
        st.write('Novos nomes:')
        st.write(valores_nao_encontrados)
        envio = material.values.tolist()  # Cria uma lista de listas a partir do DataFrame
        update_modulos(envio)
        return st.write(material)

st.title("Atualize base de dados com novos alunos para a análise de módulos:")
novos_alunos = st.file_uploader("Escolha um arquivo Excel", type=['xlsx', 'xls'], key="novos_alunos")
news_alunos(novos_alunos)