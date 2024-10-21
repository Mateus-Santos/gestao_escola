import pandas as pd
from datetime import time
from datetime import datetime
from apis.api_certificados import base_certificados
from apis.api_certificados import update_base_certificados

import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
def solicitacoes_impressos(impressos_mes_novo, planilha):
    impressos_mes_novo = impressos_mes_novo[(impressos_mes_novo['tipo_certificado'] == 'Impresso')]
    impressos_mes_novo = impressos_mes_novo.drop(columns=['data_cadastro', 'tipo_certificado', 'email', 'numero', 'formatura', 'requisitos'])
    impressos_mes_novo.insert(1, 'CÓDIGO', None)
    impressos_mes_novo.insert(3, 'MÓDULOS', None)
    impressos_mes_novo.insert(4, 'INÍCIO', None)
    impressos_mes_novo.insert(6, 'CH', None)
    impressos_mes_novo.insert(7, 'CIDADE', 'Feira de Santana')
    impressos_mes_novo = impressos_mes_novo.rename(columns={'data_fim': 'FIM', 'nome': 'NOME', 'curso': 'CURSO'})
    impressos_mes_old = pd.DataFrame(base_certificados(planilha))
    impressos_mes_old = impressos_mes_old.rename(columns={0: 'NOME', 1: 'CÓDIGO', 2: 'CURSO', 
                                                        3: 'MÓDULOS', 4: 'INÍCIO', 5: 'FIM',
                                                        6: 'CH', 7: 'CIDADE'})
    impressos_mes_atualizado = pd.concat([impressos_mes_old, impressos_mes_novo], ignore_index=True).drop_duplicates(subset=['NOME', 'CURSO'], keep='first')
    envio = impressos_mes_atualizado.values.tolist()
    return st.dataframe(update_base_certificados(planilha, envio))

def exibir_certificados_mes(ano_selecionado, mes_selecionado):
    planilha = str(ano_selecionado) + str(mes_selecionado)
    st.title(f"Planilha {mes_selecionado} de {ano_selecionado}")
    st.title(planilha)
    st.dataframe(base_certificados(planilha))
    st.title("Base de dados completa")
    formulario_forms = pd.DataFrame(base_certificados("principal"))
    formulario_forms = formulario_forms.rename(columns={0: 'data_cadastro', 1: 'email', 2: 'nome', 
                                                        3: 'curso', 4: 'data_fim', 5: 'tipo_certificado',
                                                        6: 'numero', 7: 'formatura', 8: 'requisitos'})
    st.dataframe(formulario_forms)
    formulario_forms['data_cadastro'] = pd.to_datetime(formulario_forms['data_cadastro'])
    formulario_forms['data_cadastro'] = formulario_forms['data_cadastro'].dt.strftime('%d-%m-%y')
    formulario_forms_filtro = formulario_forms[(formulario_forms['data_cadastro'] >= f'1/10/{ano_selecionado}') & (formulario_forms['data_cadastro'] <= f'31/10/{ano_selecionado}')]
    st.title("Certificados impressos:")
    solicitacoes_impressos(formulario_forms_filtro, planilha)
    return "Certificados"


st.title("Relatório de Certificados:")

col1, col2 = st.columns(2)
anos = [2021, 2022, 2023, 2024, 2025, 2026, 2027]

with col1:
    mes_selecionado = st.selectbox("Selecione o mês:", ["janeiro", "fevereiro", "marco", "abril", "maio", 
                                                    "junho", "julho", "agosto", "setembro", "outubro", 
                                                    "novembro", "dezembro"], index=datetime.now().month-1)

if datetime.now().year in anos:
    ano_atual = anos.index(datetime.now().year)
else:
    ano_atual = None

with col2:
    ano_selecionado = st.selectbox("Selecione o ano:", anos, index=ano_atual)

try:
    exibir_certificados_mes(ano_selecionado, mes_selecionado)
except FileNotFoundError:
    st.title("Base de dados não cadastrada, deseja realizar o cadastro?")