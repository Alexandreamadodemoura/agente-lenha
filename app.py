import os
import json
import base64
import requests
import google.generativeai as genai
import gspread
from flask import Flask, request

app = Flask(__name__)

# 1. Configuração do Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Configuração da Planilha (O método novo e direto do gspread)
sheet = None
try:
    encoded_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if encoded_json:
        decoded_json = base64.b64decode(encoded_json).decode('utf-8')
        creds_dict = json.loads(decoded_json)
        
        # A magia acontece aqui: o gspread faz tudo sozinho agora
        client = gspread.service_account_from_dict(creds_dict)
        sheet = client.open_by_key("1xEzT5SCZRLvcCUSeRTiCQZQZJ4SjtJXTxA_wxQVRUzY").sheet1
        print("Planilha conectada com sucesso!")
    else:
        print("Variável GOOGLE_APPLICATION_CREDENTIALS_JSON não encontrada.")
except Exception as e:
    print(f"Erro na conexão com a planilha: {e}")

# 3. A Página Inicial
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
    
    return "OK", 200

if __name__ == '__main__':
    app.run()
