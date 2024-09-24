import pandas as pd
import streamlit as st
import io

from apis.api_modulos import local_Sheets_Modulos

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
    st.dataframe(qtd_nao_entregues, hide_index=True)

entrega_Modulos()