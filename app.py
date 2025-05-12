import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

# --- Autenticação com Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Carregar credenciais do ambiente
creds_dict = {
    "type": "service_account",
    "project_id": "projeto",
    "private_key_id": "abc",
    "private_key": os.environ['GOOGLE_PRIVATE_KEY'].replace("\\n", "\n"),
    "client_email": os.environ['GOOGLE_SERVICE_ACCOUNT_EMAIL'],
    "client_id": "123",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/" + os.environ['GOOGLE_SERVICE_ACCOUNT_EMAIL'].replace('@', '%40')
}

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

sheet = client.open_by_key(os.environ['SHEET_ID']).sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

st.title("Cadastro de Documentos")

# --- Formulário ---
st.header("REGISTRO")
numero = st.text_input("Número:")
ano = st.text_input("Ano:")
tipo_doc = st.text_input("Tipo de Doc:")
modo_aquisicao = st.text_input("Modo de Aquisição:")
ano_baixa = st.text_input("Ano da Baixa:")

st.header("DADOS DO DOCUMENTO")
autor = st.text_input("Autor:")
titulo = st.text_input("Título:")
editora = st.text_input("Editora:")

st.header("LOCALIZAÇÃO NO ACERVO")
acervo = st.text_input("Acervo:")
forma = st.text_input("Forma:")
classe = st.text_input("Classe:")
assunto = st.text_input("Assunto:")
etiqueta = st.text_input("Etiqueta de Lombada:")

# --- Verificação se Número já existe ---
if numero:
    resultado = df[df["Número"] == numero]
    if not resultado.empty:
        st.success("Número encontrado. Campos preenchidos automaticamente.")
        ano = resultado.iloc[0]["Ano"]
        tipo_doc = resultado.iloc[0]["Tipo de Doc"]
        modo_aquisicao = resultado.iloc[0]["Modo de Aquisição"]
        ano_baixa = resultado.iloc[0]["Ano da Baixa"]
        autor = resultado.iloc[0]["Autor"]
        titulo = resultado.iloc[0]["Título"]
        editora = resultado.iloc[0]["Editora"]
        acervo = resultado.iloc[0]["Acervo"]
        forma = resultado.iloc[0]["Forma"]
        classe = resultado.iloc[0]["Classe"]
        assunto = resultado.iloc[0]["Assunto"]
        etiqueta = resultado.iloc[0]["Etiqueta de Lombada"]
    else:
        st.warning("Número não encontrado. Preencha os campos para cadastrar novo item.")

# --- Botão de salvar ---
if st.button("SALVAR"):
    if numero in df["Número"].values:
        st.error("Este número já existe. Não é possível sobrescrever.")
    else:
        nova_linha = [numero, ano, tipo_doc, modo_aquisicao, ano_baixa,
                      autor, titulo, editora,
                      acervo, forma, classe, assunto, etiqueta]
        sheet.append_row(nova_linha)
        st.success("Novo documento salvo com sucesso.")
