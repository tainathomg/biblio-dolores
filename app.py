import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import requests

# Configurar a largura da página
st.set_page_config(layout="wide")

# Custom CSS para os botões por texto
st.markdown("""
    <style>
    .btn-limpar {
        background-color: #f0f2f6;
        color: black;
        border: 1px solid #d3d3d3;
        padding: 0.5em 2em;
        border-radius: 8px;
        font-weight: bold;
        margin-right: 1em;
    }
    .btn-validar {
        background-color: #ffd700;
        color: black;
        border: none;
        padding: 0.5em 2em;
        border-radius: 8px;
        font-weight: bold;
        margin-right: 1em;
    }
    .btn-salvar {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5em 2em;
        border-radius: 8px;
        font-weight: bold;
    }
    h1 {
        font-size: 1.6rem !important;
    }
    h2 {
        font-size: 1.2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar estado de controle para limpar campos
if 'limpar_campos' not in st.session_state:
    st.session_state.limpar_campos = False

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

# Inicializar session state
if 'numero' not in st.session_state:
    st.session_state.numero = ""
if 'ano' not in st.session_state:
    st.session_state.ano = ""
if 'tipo_doc' not in st.session_state:
    st.session_state.tipo_doc = ""
if 'modo_aquisicao' not in st.session_state:
    st.session_state.modo_aquisicao = ""
if 'ano_baixa' not in st.session_state:
    st.session_state.ano_baixa = ""
if 'isbn' not in st.session_state:
    st.session_state.isbn = ""
if 'autor' not in st.session_state:
    st.session_state.autor = ""
if 'titulo' not in st.session_state:
    st.session_state.titulo = ""
if 'editora' not in st.session_state:
    st.session_state.editora = ""
if 'acervo' not in st.session_state:
    st.session_state.acervo = ""
if 'forma' not in st.session_state:
    st.session_state.forma = ""
if 'classe' not in st.session_state:
    st.session_state.classe = ""
if 'assunto' not in st.session_state:
    st.session_state.assunto = ""
if 'etiqueta' not in st.session_state:
    st.session_state.etiqueta = ""




def limpar_campos():
    # Limpar todos os campos
    for key in st.session_state.keys():
        st.session_state[key] = ""
    st.rerun()

def verificar_numero():
    numero = st.session_state.numero
    if numero:
        numero = str(numero).strip()
        df["Número"] = df["Número"].astype(str).str.strip()
        resultado = df[df["Número"] == numero]
        
        if not resultado.empty:
            st.session_state.ano = str(resultado.iloc[0]["Ano"]).strip()
            st.session_state.tipo_doc = str(resultado.iloc[0]["Tipo de Doc"]).strip()
            st.session_state.modo_aquisicao = str(resultado.iloc[0]["Modo de Aquisição"]).strip()
            st.session_state.ano_baixa = str(resultado.iloc[0]["Ano da Baixa"]).strip()
            st.session_state.autor = str(resultado.iloc[0]["Autor"]).strip()
            st.session_state.titulo = str(resultado.iloc[0]["Título"]).strip()
            st.session_state.editora = str(resultado.iloc[0]["Editora"]).strip()
            st.session_state.acervo = str(resultado.iloc[0]["Acervo"]).strip()
            st.session_state.forma = str(resultado.iloc[0]["Forma"]).strip()
            st.session_state.classe = str(resultado.iloc[0]["Classe"]).strip()
            st.session_state.assunto = str(resultado.iloc[0]["Assunto"]).strip()
            st.session_state.etiqueta = str(resultado.iloc[0]["Etiqueta de Lombada"]).strip()
            st.success("Número encontrado. Campos preenchidos automaticamente.")
        else:
            st.warning("Número não encontrado. Preencha os campos para cadastrar novo item.")
            # Limpar apenas os outros campos, mantendo o número
            st.session_state.ano = ""
            st.session_state.tipo_doc = ""
            st.session_state.modo_aquisicao = ""
            st.session_state.ano_baixa = ""
            st.session_state.autor = ""
            st.session_state.titulo = ""
            st.session_state.editora = ""
            st.session_state.acervo = ""
            st.session_state.forma = ""
            st.session_state.classe = ""
            st.session_state.assunto = ""
            st.session_state.etiqueta = ""


def preencher_campos_com_isbn():
    isbn = st.session_state.isbn.strip()
    if not isbn:
        return

    api_key = "AIzaSyDRGxLjAXtGRwfwbvOj9hsrLgMSo19NshI"
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "items" in data:
            volume_info = data["items"][0]["volumeInfo"]
            st.session_state.autor = ", ".join(volume_info.get("authors", []))
            st.session_state.titulo = volume_info.get("title", "")
            st.session_state.editora = volume_info.get("publisher", "")
            st.success("Informações preenchidas a partir do ISBN.")
        else:
            st.warning("ISBN não encontrado no Google Books.")
    except Exception as e:
        st.error(f"Erro ao buscar ISBN: {e}")

# Se a flag de limpeza estiver ativada, limpe os campos antes de renderizar os inputs
if st.session_state.limpar_campos:
    for key in ['numero', 'ano', 'tipo_doc', 'modo_aquisicao', 'ano_baixa', 'autor', 'titulo',
                'editora', 'acervo', 'forma', 'classe', 'assunto', 'etiqueta']:
        st.session_state[key] = ""
    st.session_state.limpar_campos = False
    st.rerun()

    
st.title("Cadastro de Livros - Biblioteca Dolores")

# --- Formulário ---
st.header("REGISTRO")
# Criar colunas para os campos do registro
cols = st.columns(5)
with cols[0]:
    st.text_input("Número:", key='numero', on_change=verificar_numero)
with cols[1]:
    st.text_input("Ano:", key='ano')
with cols[2]:
    st.text_input("Tipo de Doc:", key='tipo_doc')
with cols[3]:
    st.text_input("Modo de Aquisição:", key='modo_aquisicao')
with cols[4]:
    st.text_input("Ano da Baixa:", key='ano_baixa')

st.header("DADOS DO DOCUMENTO")
# Criar colunas para os dados do documento
cols = st.columns(4)
with cols[0]:
    st.text_input("ISBN:", key='isbn', on_change=preencher_campos_com_isbn)
with cols[1]:
    st.text_input("Autor:", key='autor')
with cols[2]:
    st.text_input("Título:", key='titulo')
with cols[3]:
    st.text_input("Editora:", key='editora')

st.header("LOCALIZAÇÃO NO ACERVO")
# Criar colunas para a localização no acervo
cols = st.columns(5)
with cols[0]:
    st.text_input("Acervo:", key='acervo')
with cols[1]:
    st.text_input("Forma:", key='forma')
with cols[2]:
    st.text_input("Classe:", key='classe')
with cols[3]:
    st.text_input("Assunto:", key='assunto')
with cols[4]:
    st.text_input("Etiqueta de Lombada:", key='etiqueta')

# Divisor mais fino e menos espaçamento
st.markdown('<hr style="margin-top: 10px; margin-bottom: 10px; border: none; border-top: 1px solid #eee;" />', unsafe_allow_html=True)

# CSS para reduzir espaçamento vertical entre elementos
st.markdown("""
    <style>
    .block-container {
        padding-bottom: 0.5rem !important;
    }
    .stButton { margin-top: 0 !important; margin-bottom: 0 !important; }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("LIMPAR", use_container_width=True, type="secondary"):
        st.session_state.limpar_campos = True
        st.rerun()
with col2:
    if st.button("VALIDAR", use_container_width=True, type="secondary"):
        numero = st.session_state.numero
        if numero:
            numero = str(numero).strip()
            df["Número"] = df["Número"].astype(str).str.strip()
            resultado = df[df["Número"] == numero]
            
            if not resultado.empty:
                # Encontrar a linha do registro no Google Sheet
                cell = sheet.find(numero)
                if cell:
                    # Atualizar a coluna Validação
                    sheet.update_cell(cell.row, 15, "Validado")  # Ajuste o número da coluna conforme necessário
                    st.success("Registro validado com sucesso!")
                    st.session_state.limpar_campos = True
                    st.rerun()
            else:
                st.error("Número não encontrado para validação.")
        else:
            st.error("Digite um número para validar.")
with col3:
    if st.button("SALVAR", use_container_width=True, type="secondary"):
        if st.session_state.numero in df["Número"].values:
            st.error("Este número já existe. Não é possível sobrescrever.")
        else:
            acervo = st.session_state.acervo or ""
            classe = st.session_state.classe or ""
            autor = (st.session_state.autor or "").upper()[:3]
            titulo = (st.session_state.titulo or "")
            titulo_letra = titulo[0].lower() if titulo else ""
            numero = st.session_state.numero or ""
            etiqueta = f"{acervo}({classe}){autor}{titulo_letra}{numero}"
            nova_linha = [st.session_state.numero, st.session_state.ano, st.session_state.tipo_doc, 
                         st.session_state.modo_aquisicao, st.session_state.ano_baixa,
                         st.session_state.autor, st.session_state.titulo, st.session_state.editora,
                         st.session_state.acervo, st.session_state.forma, st.session_state.classe, 
                         st.session_state.assunto, etiqueta, "Validado"]
            sheet.append_row(nova_linha)
            st.success(f"Novo documento salvo com sucesso. Etiqueta de Lombada: {etiqueta}")
            st.session_state.limpar_campos = True
            st.rerun()

