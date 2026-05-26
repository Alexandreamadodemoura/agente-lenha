import os
import json
import gspread
from flask import Flask, request, jsonify
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Configuração da planilha via Variável de Ambiente
creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
creds_dict = json.loads(creds_json)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1xEzT5SCZRLvcCUSeRTiCQZQZJ4SjtJXTxA_wxQVRUzY").sheet1

@app.route('/')
def home():
    return "Agente de Lenha está Online!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Validação da Meta
        token = request.args.get('hub.verify_token')
        if token == "lenha_agente_secreto_2026":
            return request.args.get('hub.challenge')
        return "Token inválido", 403
    
    # Processamento de mensagens
    data = request.json
    print(data) 
    return "OK", 200

if __name__ == '__main__':
    app.run()
