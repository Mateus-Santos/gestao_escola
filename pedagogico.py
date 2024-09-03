import pandas as pd
import streamlit as st

def relatorio_Dda():
    df = pd.read_excel('relatorio_integracao/Resultado.xls')

    filtro_colunas = df[(df['Status'] == 'Ativo') & (df['Pós venda'] == 'Sim') & (df['Participação DDA'] == 'Não')][['Aluno', 'Telefone Celular']]

    filtro_colunas.to_excel('listasender.xlsx', index=False)
    # Converter o DataFrame para CSV
    filtro_colunas.to_csv('listasender.csv', index=False, encoding='utf-8', sep=';')

    csv = filtro_colunas.to_csv(index=False, encoding='utf-8', sep=';')

    print(filtro_colunas)

    st.write("""
        ##Gráfico do App
        O gráfico da quantidade de contatos.
    """)

    st.download_button(
        label="Baixar CSV",
        data=csv.encode('utf-8'),
        file_name='integracaodda.csv',
        mime='text/csv'
    )

    # st.table(filtro_colunas)
    # st.dataframe(filtro_colunas)
    st.write(filtro_colunas)