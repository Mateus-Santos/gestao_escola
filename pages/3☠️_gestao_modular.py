import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os, sys, json
from dotenv import load_dotenv
from datetime import datetime, time
from utils.update_database import update_database
from apis.api_sheets import local_Sheets, update_sheets
from services.services_modular import atualizar_vagas_turmas

def main():
    print("Tela de Gestão Modular")
    st.title("Atualize turmas modular")
    planilha_turmas = st.file_uploader("Escolha um arquivo Excel", type=['xlsx', 'xls'], key="planilha_turmas")
    local_planilha = f'./database/bases de dados/retencao/turmas_atual.xls'
    if planilha_turmas:
        update_database(local_planilha, planilha_turmas)    
        atualizar_vagas_turmas(planilha_turmas)
        
main()