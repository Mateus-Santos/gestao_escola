import streamlit as st
from docx import Document
from io import BytesIO
from docx2pdf import convert
import os
import pythoncom

st.title("Emitir termos para solicitação de certificado Digital:")

col1, col2, col3 = st.columns(3)

def gerar_pdf(local_doc, nome):
    pythoncom.CoInitialize()
    try:
        caminho_docx = f"{local_doc}/{nome}_TERMO_CERTIFICADO_DIGITAL.docx"
        caminho_pdf = f"{local_doc}/{nome}_TERMO_CERTIFICADO_DIGITAL.pdf"
        convert(caminho_docx, caminho_pdf)
        print(f"PDF GERADO COM SUCESSO EM: {caminho_pdf}")
    finally:
        pythoncom.CoUninitialize()

def emitir_termo(doc_path):
    with st.form("Meu formulário"):
        nome = st.text_input("Insira o Nome Completo")
        cpf = st.text_input("Insira o CPF")
        curso = st.text_input("Insira o Curso")
        submit_button = st.form_submit_button("Gerar Documento")
        
    if submit_button:
        doc = Document(doc_path)
        variaveis = {
            "nome": nome,
            "cpf": cpf,
            "curso": curso,
        }

        for paragrafo in doc.paragraphs:
            for run in paragrafo.runs:
                for chave, valor in variaveis.items():
                    if f"{{{{{chave}}}}}" in run.text:
                        run.text = run.text.replace(f"{{{{{chave}}}}}", valor)
        os.makedirs("./database/modular/termos", exist_ok=True)
        doc.save(f"./database/modular/termos/{nome}_TERMO_CERTIFICADO_DIGITAL.docx")
        gerar_pdf(f"./database/modular/termos/", nome)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button(
            label="Baixar Docx",
            data=buffer,
            file_name=f"{nome}_TERMO_CERTIFICADO_DIGITAL.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        st.download_button(
            label="Baixar PDF",
            data=open(f"./database/modular/termos/{nome}_TERMO_CERTIFICADO_DIGITAL.pdf", "rb").read(),
            file_name=f"{nome}_TERMO_CERTIFICADO_DIGITAL.pdf",
            mime="application/pdf"
        )

st.write("Você pode preencher o termo, aqui:")
input_word = './database/modular/termos/TERMO_CERTIFICADO_DIGITAL.docx'
emitir_termo(input_word)