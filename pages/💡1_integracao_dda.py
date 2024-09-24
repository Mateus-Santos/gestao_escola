import pandas as pd
import streamlit as st

from main import update_database

def relatorio_Dda():
    # Mensagem para atualizar a base de dados integração DDA.
    st.title("Atualize a base de dados do relatório de integração DDA.")
    base_relatorio_dda = st.file_uploader("Escolha um arquivo Excel", type=['xlsx', 'xls'], key="base_relatorio_dda")
    update_database('./database/modular/relatorio_integracao/Resultado.xls', base_relatorio_dda)
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

    st.dataframe(filtro_colunas, hide_index=True)

relatorio_Dda()