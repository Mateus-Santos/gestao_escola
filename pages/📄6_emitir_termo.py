import streamlit as st
from docx import Document
from io import BytesIO


st.title("Emitir termos para solicitação de certificado Digital:")

col1, col2, col3 = st.columns(3)

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
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)        
        st.download_button(
            label="Baixar Documento",
            data=buffer,
            file_name=f"{nome}_TERMO_CERTIFICADO_DIGITAL.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

st.write("Você pode preencher o termo, aqui:")
input_word = './database/modular/termos/TERMO_CERTIFICADO_DIGITAL.docx'
emitir_termo(input_word)