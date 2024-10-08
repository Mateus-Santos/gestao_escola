import pandas as pd
import streamlit as st
import io

from apis.api_modulos import local_Sheets_Modulos
from apis.api_modulos import update_modulos

def entrega_Modulos():
    gsheets = local_Sheets_Modulos()
    colunas = gsheets[0]
    material = pd.DataFrame(data=gsheets, columns=colunas)
    material = material[1:].reset_index(drop=True)
    qtd_nao_entregues = material.apply(lambda col: col.value_counts().get('O', 0))
    excel_buffer = io.BytesIO()
    material.to_excel(excel_buffer, index=False, engine='xlsxwriter')
    excel_buffer.seek(0)
    excel_buffer.truncate(0)
    excel_buffer.seek(0)
    qtd_nao_entregues.to_excel(excel_buffer, index=True, engine='xlsxwriter')
    excel_buffer.seek(0)
    st.title('Lista com a quantidade de Módulos para solicitar')
    st.download_button(
        label="Baixar Lista Completa",
        data=excel_buffer,
        file_name='Lista de Modulos.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        key='material'
    )
    st.download_button(
        label="Baixar Relatório de Módulos",
        data=excel_buffer,
        file_name='Relatorio_de_Modulos_a_Entregar.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        key='qtd_nao_entregues'
    )
    st.dataframe(qtd_nao_entregues)

def news_alunos(novos_alunos):
    if novos_alunos is not None:
        df = pd.read_excel(novos_alunos)
        novos_alunos_df = df[(df['Status'] == 'Ativo') & (df['Tipo Contrato'] == 'Interativo')]
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
entrega_Modulos()
news_alunos(novos_alunos)