import pandas as pd
import streamlit as st
import time
import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Carregar os contatos do Excel
contatos_df = pd.read_excel("Enviar.xlsx")
st.dataframe(contatos_df)

# Configurar o navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
navegador.get("https://web.whatsapp.com/")

try:
    WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.ID, "side")))
    st.success("Login realizado com sucesso no WhatsApp Web!")
    time.sleep(5)
except TimeoutException:
    st.error("Erro: Não foi possível detectar o login no WhatsApp Web. Verifique sua conexão e tente novamente.")
    navegador.quit()

# Enviar mensagens
for i, mensagem in enumerate(contatos_df['Mensagem']):
    pessoa = contatos_df.loc[i, "Pessoa"]
    numero = contatos_df.loc[i, "Número"]
    texto = urllib.parse.quote(f"Olá, eu falo com a responsável pelo curso de {pessoa}? {mensagem}")
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
    navegador.get(link)

    try:
        campo_mensagem = WebDriverWait(navegador, 40).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[3]/div[1]/p'))
        )
        time.sleep(2)
        campo_mensagem.click()
        campo_mensagem.send_keys(Keys.ENTER)
        st.success(f"Mensagem enviada para {pessoa} ({numero})")
        time.sleep(10)
    except TimeoutException:
        st.error(f"Erro: Não foi possível enviar a mensagem para {pessoa} ({numero}).")
        continue
    except NoSuchElementException:
        st.error(f"Erro: Elemento da mensagem não encontrado para {pessoa} ({numero}).")
        continue

st.success("Envio finalizado!")
navegador.quit()