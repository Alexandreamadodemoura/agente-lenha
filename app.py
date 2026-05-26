import os
import json
import gspread
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Configuração segura
creds_json_str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")

if creds_json_str:
    try:
        creds_dict = json.loads(creds_json_str.strip()) # O .strip() remove espaços acidentais
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1xEzT5SCZRLvcCUSeRTiCQZQZJ4SjtJXTxA_wxQVRUzY").sheet1
    except Exception as e:
        print(f"Erro ao configurar Planilha: {e}")
        sheet = None
else:
    print("Variável GOOGLE_APPLICATION_CREDENTIALS_JSON não encontrada!")
    sheet = None

@app.route('/')
def home():
    return "Agente de Lenha Ativo!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == "lenha_agente_secreto_2026":
            return request.args.get('hub.challenge')
        return "Token inválido", 403
    
    data = request.json
    print(data) 
    return "OK", 200
