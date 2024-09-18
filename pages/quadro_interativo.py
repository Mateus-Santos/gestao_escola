import pandas as pd
from datetime import time

agendamento = pd.read_excel('horarios.xlsx', sheet_name='agendamento')

agendamento['INICIO'] = pd.to_datetime(agendamento['INICIO'], format='%H:%M:%S').dt.time
agendamento['FIM'] = pd.to_datetime(agendamento['FIM'], format='%H:%M:%S').dt.time

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
        time(18, 0, 0): '',
        },
    'SEX': {
        time(8, 0, 0): '',
        time(10, 0, 0): '',
        time(13, 0, 0): '',
        time(15, 0, 0): '',
        time(18, 0, 0): '',
        },
    'SAB': {
        time(8, 0, 0): '',
        time(10, 0, 0): '',
        time(13, 0, 0): '',
        time(15, 0, 0): '',
        time(18, 0, 0): '',
        },
}

for dia in quadro:
    quadro[dia][time(8, 0, 0)] = agendamento[((agendamento['DIA'] == dia)) & (agendamento['INICIO'] >= time(8, 0, 0)) & (agendamento['INICIO'] < time(10, 0, 0))]['DIA'].value_counts().sum()
    quadro[dia][time(10, 0, 0)] = agendamento[((agendamento['DIA'] == dia)) & (agendamento['INICIO'] >= time(10, 0, 0)) & (agendamento['INICIO'] < time(12, 0, 0))]['DIA'].value_counts().sum()
    quadro[dia][time(13, 0, 0)] = agendamento[((agendamento['DIA'] == dia)) & (agendamento['INICIO'] >= time(13, 0, 0)) & (agendamento['INICIO'] < time(15, 0, 0))]['DIA'].value_counts().sum()
    quadro[dia][time(15, 0, 0)] = agendamento[((agendamento['DIA'] == dia)) & (agendamento['INICIO'] >= time(15, 0, 0)) & (agendamento['INICIO'] < time(17, 0, 0))]['DIA'].value_counts().sum()
    quadro[dia][time(18, 0, 0)] = agendamento[((agendamento['DIA'] == dia)) & (agendamento['INICIO'] >= time(18, 0, 0)) & (agendamento['INICIO'] < time(20, 0, 0))]['DIA'].value_counts().sum()

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