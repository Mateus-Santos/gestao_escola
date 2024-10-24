import pandas as pd
import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))   

def relatorio_alunos(base_contratos, base_grades):
    contratos = pd.read_excel(base_contratos)
    grade = pd.ExcelFile(base_grades)
    contratos = contratos.drop(columns=['CPF', 'Assinatura Digital', 'Data Inicial', 'Tipo Pré-atendimento', 
                                            'Status Pedagógico', 'Mês Nasc.', 'Data Nasc.', 'Idade', 'Sexo', 'Endereço', 'Bairro', 'Cidade', 
                                             'Data Cadastro', 'Mídia', 'Campanha', 'Campanha Franquia', 'Consultor', 'Gerador', 'Assistente de Mídia', 
                                             'Última Alteração de Status', 'Responsável Legal', 'Financeiro Legal', 'Mês Nasc Resp Fin.', 'SCPC', 'Cobranca Terceirizada',
                                             'Curso à vista', 'Recorrente', 'Cartão de crédito', 'Cartório', 'Serasa', 'Procon', 'Processo Jurídico', 'Nº de Parcelas', 
                                             'Receb. Atrasados', 'Matrículas Atrasadas', 'Parcelas Atrasadas', 'Mat. Didatico Atrasados'])
    st.title("Planilha de dados interativo")
    st.dataframe(contratos)
    st.title("Planilhas de grades cursos Interasoft")
    
    # Obter todos os nomes das planilhas
    planilhas = grade.sheet_names

    # Iterar sobre as planilhas e carregar os dados
    st.title(f"Veja todas as grades dos cursos:")
    for planilha in planilhas:
        df_grade = pd.read_excel(grade, sheet_name=planilha)
        st.write(f"Dados da planilha {planilha}:")
        st.dataframe(df_grade)

try:
    relatorio_alunos('./database/interativo/base_interativo.xls', './database/interativo/grade_interasoft.xlsx')
except FileNotFoundError:
    st.title("Base de dados não cadastrada, deseja realizar o cadastro?")