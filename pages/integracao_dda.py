import pandas as pd
import streamlit as st

def relatorio_Dda():
    df = pd.read_excel('./database/modular/relatorio_integracao/Resultado.xls')

    filtro_colunas = df[(df['Status'] == 'Ativo') & (df['Pós venda'] == 'Sim') & (df['Participação DDA'] == 'Não')][['Aluno', 'Telefone Celular']]
    
    csv = filtro_colunas.to_csv(index=False, encoding='utf-8', sep=';')

    st.title("Integração alunos DDA")

    st.write("""
        Tabela de alunos de Pós venda, sem DDA.
    """)
    
    st.download_button(
        label="Baixar CSV",
        data=csv.encode('utf-8'),
        file_name='integracaodda.csv',
        mime='text/csv'
    )

    st.write(filtro_colunas)

relatorio_Dda()