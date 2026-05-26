import os
import json
import base64
import requests
import google.generativeai as genai
import gspread
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# 1. Configuração do Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Configuração da Planilha (via Base64)
sheet = None
try:
    encoded_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if encoded_json:
        decoded_json = base64.b64decode(encoded_json).decode('utf-8')
        creds_dict = json.loads(decoded_json)
        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1xEzT5SCZRLvcCUSeRTiCQZQZJ4SjtJXTxA_wxQVRUzY").sheet1
        print("Planilha conectada com sucesso!")
    else:
        print("Variável GOOGLE_APPLICATION_CREDENTIALS_JSON não encontrada.")
except Exception as e:
    print(f"Erro na conexão com a planilha: {e}")

# 3. A Página Inicial (A que estava a faltar e gerou o erro!)
@app.route('/')
def home():
    status = "conectada" if sheet else "NÃO conectada"
    return f"Agente de Lenha Ativo! Planilha: {status}", 200

# 4. A porta do WhatsApp (Webhook)
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == "lenha_agente_secreto_2026":
            return request.args.get('hub.challenge')
        return "Token inválido", 403
    
    # Aqui entrará a lógica de ler a foto mais tarde
    return "OK", 200

if __name__ == '__main__':
    app.run()
