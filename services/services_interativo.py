import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os, sys, json
from dotenv import load_dotenv
from datetime import datetime, time
from utils.update_database import update_database
from apis.api_sheets import local_Sheets, update_sheets

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)

def gerar_relatorio_assiduidade(local_planilha):
    assiduidade = pd.read_excel(local_planilha)
    assiduidade = assiduidade.drop(columns=['Contato Emergência 1', 'Contato Emergência 2', 
                                            'Contato Emergência 3', 'Contato Emergência 4', 
                                            'Contrato', 'Telefone Aluno', 'Data', 'Reposições', 'Status'])
    ranking_frequentes = assiduidade.sort_values(by='Presenças', ascending=False)
    ranking_frequentes['Total'] = ranking_frequentes['Presenças'] + ranking_frequentes['Faltas']
    ranking_frequentes['Frequencia'] = (ranking_frequentes['Presenças'] / ranking_frequentes['Total']) * 100
    ranking_frequentes['Frequencia'] = ranking_frequentes['Frequencia'].replace(['inf%', '-inf%'], '0%')
    ranking_frequentes = ranking_frequentes.sort_values(by='Frequencia', ascending=False)
    presenca = ranking_frequentes['Presenças'].sum()
    falta = ranking_frequentes['Faltas'].sum()
    dados_pizza = {
    'Presença': presenca,
    'Falta': falta,
    }
    cores = ['#00FF00','#FF0000']
    # Criar o gráfico de pizza
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.pie(dados_pizza.values(), labels=dados_pizza.keys(), 
        autopct='%1.1f%%', 
        startangle=70, 
        colors=cores, textprops={'fontsize': 7})
    ax.set_title('Assiduidade - Interativo', fontsize=12)
    fig.patch.set_facecolor('white')
    st.pyplot(fig)
    return ranking_frequentes

#Gerar lista de alunos com muitas faltas consecutivas durante mês.
def listar_faltantes_retencao(local_arquivo):
    assiduidade = pd.read_excel(local_arquivo)
    assiduidade = assiduidade.drop(columns=['Contato Emergência 1', 'Contato Emergência 2', 
                                            'Contato Emergência 3', 'Contato Emergência 4', 
                                            'Contrato', 'Data', 'Reposições', 'Presenças'])
    faltantes = assiduidade[(assiduidade['Status'] == 'Ativo') & (assiduidade['Faltas'] >= 2)]
    faltantes = faltantes.drop(columns=['Status'])
    csv = faltantes.to_csv(index=False, encoding='utf-8', sep=';')
    return [faltantes, csv]

#API só funcionará a cada 7 dias.
@st.cache_data(ttl=604800)
def plotar_grafico_assiduidade():
    ano_inicial = 2022
    hoje = datetime.today()
    ano_atual, mes_atual = hoje.year, hoje.month
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", 
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

    dados = {"Mês": [], "Assiduidade": []}
    
    for ano in range(ano_inicial, ano_atual + 1):
        for mes_idx, mes_nome in enumerate(meses, start=1):
            if ano == ano_atual and mes_idx > mes_atual:
                break
            try:
                arquivo = pd.DataFrame(local_Sheets(f'{ano}{mes_nome}!A2:L1000', os.getenv("ID_PLANILHA_INTERATIVO")))
                arquivo = arquivo.rename(columns={0: 'CONTRATO', 1: 'NOME', 2: 'STATUS', 3: 'TEL1', 4: 'Presenças', 5: 'Faltas', 6: 'Reposições'})
                arquivo['Presenças'] = arquivo['Presenças'].astype(int)
                arquivo['Faltas'] = arquivo['Faltas'].astype(int)
                arquivo['Total'] = arquivo['Presenças'] + arquivo['Faltas']
                presencas_mes = arquivo['Presenças'].sum()
                total_chamadas = arquivo['Total'].sum()
                assiduidade = (presencas_mes/total_chamadas) * 100
                dados["Mês"].append(f"{mes_nome}/{ano}")
                dados["Assiduidade"].append(round(assiduidade, 2))

            except Exception as e:
                print(f"Planilha não encontrada: {ano}{mes_nome}: {e}")

    df_final = pd.DataFrame(dados)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_final["Mês"], df_final["Assiduidade"], marker="o", linestyle="-", color="b", label="assiduidade")

    for i, txt in enumerate(df_final["Assiduidade"]):
        ax.text(i, txt + 1, f"{txt}%", ha="center", fontsize=10, fontweight="bold", color="black")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Assiduidade (%)")
    ax.set_title("Assiduidade por Mês")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Função para exibir vagas no interativo.
def exibir_vagas():
    # Carrega os dados da planilha
    agendamento = pd.DataFrame(local_Sheets(
        os.getenv("PLANILHA_AGENDAMENTOS_INTERATIVO"),
        os.getenv("ID_PLANILHA_INTERATIVO")
    ))
    # Renomeia colunas
    agendamento.columns = ['NOME', 'DIA', 'INICIO', 'FIM', 'REPOSICAO', 'DATA']
    # Converte horários para datetime.time
    agendamento['INICIO'] = pd.to_datetime(agendamento['INICIO'], format='%H:%M:%S').dt.time
    agendamento['FIM'] = pd.to_datetime(agendamento['FIM'], format='%H:%M:%S').dt.time
    # Define horários fixos
    horarios = [
        (time(8, 0), time(10, 0)),
        (time(10, 0), time(12, 0)),
        (time(13, 0), time(15, 0)),
        (time(15, 0), time(17, 0)),
        (time(18, 0), time(20, 0)),
    ]
    dias_semana = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB']
    vagas_por_horario = 9
    # Define horários disponíveis por dia
    quadro = {dia: {inicio: vagas_por_horario for inicio, _ in horarios} for dia in dias_semana}
    # Mapa de indisponibilidades por dia
    indisponiveis = {
        'SEX': [time(8, 0), time(10, 0), time(13, 0), time(15, 0), time(18, 0)],
        'QUI': [time(18, 0)],
        'SAB': [time(13, 0), time(15, 0), time(18, 0)],
    }

    for dia in dias_semana:
        for inicio, fim in horarios:
            if inicio in quadro[dia]:
                count = agendamento[
                    (agendamento['DIA'] == dia) &
                    (agendamento['INICIO'] >= inicio) &
                    (agendamento['INICIO'] < fim)
                ].shape[0]
                quadro[dia][inicio] = vagas_por_horario - count

        # Marca horários indisponíveis como -1
        for hora_indisp in indisponiveis.get(dia, []):
            if hora_indisp in quadro[dia]:
                quadro[dia][hora_indisp] = -1

    df_quadro = pd.DataFrame(quadro)
    df_quadro['HORÁRIO INÍCIO'] = [h[0] for h in horarios]
    df_quadro['HORÁRIO FIM'] = [h[1] for h in horarios]

    # Reorganiza colunas para que horários fiquem na frente
    colunas = ['HORÁRIO INÍCIO', 'HORÁRIO FIM'] + dias_semana
    df_quadro = df_quadro[colunas]

    # Formata horários
    df_quadro['HORÁRIO INÍCIO'] = df_quadro['HORÁRIO INÍCIO'].apply(lambda x: x.strftime('%H:%M:%S'))
    df_quadro['HORÁRIO FIM'] = df_quadro['HORÁRIO FIM'].apply(lambda x: x.strftime('%H:%M:%S'))
    update_sheets(df_quadro.values.tolist(), os.getenv("PLANILHA_VAGAS_INTERATIVO"), os.getenv("ID_PLANILHA_INTERATIVO"))

    return df_quadro

def pendente_reposicoes():
    agendamento = pd.DataFrame(local_Sheets(
        os.getenv("PLANILHA_AGENDAMENTOS_INTERATIVO"),
        os.getenv("ID_PLANILHA_INTERATIVO")
    ))
    agendamento.columns = ['NOME', 'DIA', 'INICIO', 'FIM', 'REPOSICAO', 'DATA']
    agendamento['DATA'] = pd.to_datetime(agendamento['DATA'], format="%d/%m/%Y", errors='coerce')
    agendamento = agendamento[agendamento['DATA'].notna()]
    data_atual = pd.Timestamp.today().normalize()
    st.write(data_atual)
    df_passadas = agendamento[agendamento['DATA'] < data_atual]
    return df_passadas
