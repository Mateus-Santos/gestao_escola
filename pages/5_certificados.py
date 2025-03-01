import pandas as pd
from datetime import datetime
from apis.api_certificados import base_certificados
from apis.api_certificados import update_base_certificados
from apis.dicionarios import mes_number
import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def solicitacoes_digitais(digitais_mes_novo, planilha):
    digitais_mes_novo = digitais_mes_novo[(digitais_mes_novo['tipo_certificado'] == 'Digital')]
    digitais_mes_novo = digitais_mes_novo.drop(columns=['data_fim', 'data_cadastro', 'tipo_certificado', 'email', 'numero', 'formatura', 'requisitos'])
    digitais_mes_novo = digitais_mes_novo.rename(columns={'nome': 'NOME', 'curso': 'CURSO'})
    digitais_mes_novo.insert(1, 'CÓDIGO', None)
    digitais_mes_old = pd.DataFrame(base_certificados(planilha))
    digitais_mes_old = digitais_mes_old.rename(columns={0: 'NOME', 1: 'CÓDIGO', 2: 'CURSO', 3: 'ASSINATURA_TERMO'})
    digitais_mes_atualizado = pd.concat([digitais_mes_old, digitais_mes_novo], ignore_index=True).drop_duplicates(subset=['NOME', 'CURSO'], keep='first')
    digitais_mes_atualizado.fillna('', inplace=True)
    envio = digitais_mes_atualizado.values.tolist()
    digitais = pd.DataFrame(update_base_certificados(planilha, envio))
    digitais = digitais.rename(columns={0: 'NOME', 1: 'CÓDIGO', 2: 'CURSO', 3: 'ASSINATURA_TERMO'})
    return digitais

def adicionar_modulos_ch(impressos_mes_atualizado):
    grade = pd.DataFrame(base_certificados('GRADE'))
    grade = grade.rename(columns={0: 'CURSO', 1: 'MÓDULOS', 2: 'CH'})
    grade = grade[['CURSO', 'MÓDULOS', 'CH']]
    impressos_mes_atualizado['MÓDULOS'] = impressos_mes_atualizado['CURSO'].map(grade.set_index('CURSO')['MÓDULOS'])
    impressos_mes_atualizado['CH'] = impressos_mes_atualizado['CURSO'].map(grade.set_index('CURSO')['CH'])
    return impressos_mes_atualizado
    
def adicionar_formatura(formatura_forms, planilha):
    old_formatura_df = pd.DataFrame(base_certificados(planilha))
    old_formatura_df = old_formatura_df.rename(columns={0: 'nome', 1: 'curso', 2: 'numero'})
    old_formatura_df = old_formatura_df[['nome', 'curso', 'numero']]
    formatura_forms = formatura_forms.drop(columns=['data_fim', 'data_cadastro', 'tipo_certificado', 'email', 'requisitos'])
    formatura_forms = formatura_forms[(formatura_forms['formatura'] == 'Sim')]
    news_formatura_forms = pd.DataFrame(pd.concat([old_formatura_df, formatura_forms], ignore_index=True).drop_duplicates(subset=['nome', 'curso', 'numero'], keep='first'))
    news_formatura_forms = news_formatura_forms.drop(columns=['formatura'])
    news_formatura_forms.fillna('', inplace=True)
    envio = news_formatura_forms.values.tolist()
    formatura = pd.DataFrame(update_base_certificados(planilha, envio))
    formatura = formatura.rename(columns={0: 'NOME', 1: 'CURSO', 2: 'NÚMERO'})
    return formatura

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
    #Atualizar módulos e carga horária.
    impressos_mes_atualizado = adicionar_modulos_ch(impressos_mes_atualizado)
    impressos_mes_atualizado.fillna('', inplace=True)
    envio = impressos_mes_atualizado.values.tolist()
    impressos = pd.DataFrame(update_base_certificados(planilha, envio))
    impressos = impressos.rename(columns={0: 'NOME', 1: 'CÓDIGO', 2: 'CURSO', 
                                                        3: 'MÓDULOS', 4: 'INÍCIO', 5: 'FIM',
                                                        6: 'CH', 7: 'CIDADE'})
    return impressos

def exibir_certificados_mes(ano_selecionado, mes_selecionado):
    planilha = str(ano_selecionado) + str(mes_selecionado)
    formulario_forms = pd.DataFrame(base_certificados("principal"))
    formulario_forms = formulario_forms.rename(columns={0: 'data_cadastro', 1: 'email', 2: 'nome', 
                                                        3: 'curso', 4: 'data_fim', 5: 'tipo_certificado',
                                                        6: 'numero', 7: 'formatura', 8: 'requisitos'})
    formulario_forms['data_cadastro'] = pd.to_datetime(formulario_forms['data_cadastro'], dayfirst=True)
    mes = mes_number(mes_selecionado)
    formulario_forms_filtro = formulario_forms[
        (formulario_forms['data_cadastro'].dt.year == ano_selecionado) &
        (formulario_forms['data_cadastro'].dt.month == mes)
    ]

    st.write(f"Certificados {mes_selecionado} impressos:")
    st.dataframe(solicitacoes_impressos(formulario_forms_filtro, planilha))
    st.write(f"Certificados {mes_selecionado} Digital:")
    st.dataframe(solicitacoes_digitais(formulario_forms_filtro, 'solicitados_digital'))
    st.write(f"Interesse na formatura:")
    st.dataframe(adicionar_formatura(formulario_forms_filtro, 'formatura'))
    

st.title("Relatório de Certificados:")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

anos = [2021, 2022, 2023, 2024, 2025, 2026, 2027]

with col1:
    mes_selecionado = st.selectbox("Selecione o mês:", ["janeiro", "fevereiro", "março", "abril", "maio", 
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