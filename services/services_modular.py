import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os, sys, json
from dotenv import load_dotenv
from datetime import datetime, time
from utils.update_database import update_database
from apis.api_sheets import local_Sheets, update_sheets

def atualizar_vagas_turmas(planilha_turmas):
    turmas = pd.read_excel(planilha_turmas)
    cursos_dfs = {
        curso: grupo.reset_index(drop=True)
        for curso, grupo in turmas.groupby('Curso')
    }
    #Criando dataframe por curso
    for i in range(len(cursos_dfs)):
        st.write(cursos_dfs[list(cursos_dfs.keys())[i]])