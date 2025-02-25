import pandas as pd
from datetime import time
import streamlit as st
import json
from apis.api_quadro import local_Sheets
from apis.api_quadro import update_quadro

def exibir_vagas():
    agendamento = pd.DataFrame(local_Sheets('agendamentos', '1QMbkbuZNg87ecpQiaRs_rEV7egNm23DNb_ARkJ31YaI'))
    agendamento = agendamento.rename(columns={0: 'NOME', 1: 'DIA', 2: 'INICIO', 3: 'FIM', 4: 'REPOSICAO', 5: 'DATA'})
    #Transformando no tipo horas.
    agendamento['INICIO'] = pd.to_datetime(agendamento['INICIO'], format='%H:%M:%S').dt.time
    agendamento['FIM'] = pd.to_datetime(agendamento['FIM'], format='%H:%M:%S').dt.time

    #Criando quadro Fixo para visualização.
    quadro = {
        'SEG': {
            time(8, 0, 0): '',
            time(10, 0, 0): '',
            time(13, 0, 0): '',
            time(15, 0, 0): '',
            time(18, 0, 0): '',
            },
        'TER': {
            time(8, 0): '',
            time(10, 0): '',
            time(13, 0): '',
            time(15, 0): '',
            time(18, 0, 0): '',
            },
        'QUA': {
            time(8, 0, 0): '',
            time(10, 0, 0): '',
            time(13, 0, 0): '',
            time(15, 0, 0): '',
            time(18, 0, 0): '',
            },
        'QUI': {
            time(8, 0, 0): '',
            time(10, 0, 0): '',
            time(13, 0, 0): '',
            time(15, 0, 0): '',
            },
        'SEX': {
            time(8, 0, 0): '',
            time(10, 0, 0): '',
            time(13, 0, 0): '',
            time(15, 0, 0): '',
            },
        'SAB': {
            time(8, 0, 0): '',
            time(10, 0, 0): '',
            },
    }
    #Definindo a quantiade de vagas.
    vagas = 8
    for dia in quadro:
        quadro[dia][time(8, 0, 0)] = vagas - agendamento[((agendamento['DIA'] == dia)) & (agendamento['INICIO'] >= time(8, 0, 0)) & (agendamento['INICIO'] < time(10, 0, 0))]['DIA'].value_counts().sum()
        quadro[dia][time(10, 0, 0)] = vagas - agendamento[((agendamento['DIA'] == dia)) & (agendamento['INICIO'] >= time(10, 0, 0)) & (agendamento['INICIO'] < time(12, 0, 0))]['DIA'].value_counts().sum()
        quadro[dia][time(13, 0, 0)] = vagas - agendamento[((agendamento['DIA'] == dia)) & (agendamento['INICIO'] >= time(13, 0, 0)) & (agendamento['INICIO'] < time(15, 0, 0))]['DIA'].value_counts().sum()
        quadro[dia][time(15, 0, 0)] = vagas - agendamento[((agendamento['DIA'] == dia)) & (agendamento['INICIO'] >= time(15, 0, 0)) & (agendamento['INICIO'] < time(17, 0, 0))]['DIA'].value_counts().sum()
        quadro[dia][time(18, 0, 0)] = vagas - agendamento[((agendamento['DIA'] == dia)) & (agendamento['INICIO'] >= time(18, 0, 0)) & (agendamento['INICIO'] < time(20, 0, 0))]['DIA'].value_counts().sum()
        #Definindo dias que não estão disponíveis:
        if dia == 'SEX':
            quadro[dia][time(8, 0, 0)] = -1
            quadro[dia][time(10, 0, 0)] = -1
            quadro[dia][time(13, 0, 0)] = -1
            quadro[dia][time(15, 0, 0)] = -1
        if dia == 'TER':
            quadro[dia][time(10, 0, 0)] = -1
        if dia == 'SEX' or dia == 'QUI':
            quadro[dia][time(18, 0, 0)] = -1
        if dia == 'SAB':
            quadro[dia][time(13, 0, 0)] = -1
            quadro[dia][time(15, 0, 0)] = -1
            quadro[dia][time(18, 0, 0)] = -1

    inicio = [
        time(8, 0, 0),
        time(10, 0, 0),
        time(13, 0, 0),
        time(15, 0, 0),
        time(18, 0, 0),
    ]

    fim = [
        time(10, 0, 0),
        time(12, 0, 0),
        time(15, 0, 0),
        time(17, 0, 0),
        time(20, 0, 0),
    ]

    new_quadro = pd.DataFrame(quadro)

    new_quadro['HORÁRIO INÍCIO'] = inicio
    new_quadro['HORÁRIO FIM'] = fim
    colunas = new_quadro.columns.tolist()
    # Mover as duas últimas colunas para o início
    nova_ordem_colunas = colunas[-2:] + colunas[:-2]
    quadro = new_quadro[nova_ordem_colunas]
    st.title("Vagas Disponíveis - Interativo")
    st.dataframe(quadro, hide_index=True)
    quadro['HORÁRIO INÍCIO'] = quadro['HORÁRIO INÍCIO'].apply(lambda x: x.strftime('%H:%M:%S'))
    quadro['HORÁRIO FIM'] = quadro['HORÁRIO FIM'].apply(lambda x: x.strftime('%H:%M:%S'))
    envio = quadro.values.tolist()
    update_quadro(envio)

exibir_vagas()