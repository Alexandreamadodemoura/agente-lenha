import os
import json
import gspread
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Tenta carregar a chave, mas não trava se falhar
sheet = None
try:
    creds_json_str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if creds_json_str:
        creds_dict = json.loads(creds_json_str.strip())
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1xEzT5SCZRLvcCUSeRTiCQZQZJ4SjtJXTxA_wxQVRUzY").sheet1
        print("Planilha conectada com sucesso!")
    else:
        print("AVISO: Variável GOOGLE_APPLICATION_CREDENTIALS_JSON não encontrada.")
except Exception as e:
    print(f"Erro ao configurar Planilha: {e}")

@app.route('/')
def home():
    status = "conectada" if sheet else "NÃO conectada"
    return f"Agente de Lenha Ativo! Planilha: {status}", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == "lenha_agente_secreto_2026":
            return request.args.get('hub.challenge')
        return "Token inválido", 403
    return "OK", 200
