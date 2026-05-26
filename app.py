import os
import requests
import google.generativeai as genai
import gspread
from flask import Flask, request

app = Flask(__name__)

# 1. Configuração do Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Configuração da Planilha (Via Secret File do Render)
sheet = None
try:
    # O gspread vai ler o arquivo diretamente da pasta segura do Render
    caminho_arquivo = '/etc/secrets/credentials.json'
    
    client = gspread.service_account(filename=caminho_arquivo)
    sheet = client.open_by_key("1xEzT5SCZRLvcCUSeRTiCQZQZJ4SjtJXTxA_wxQVRUzY").sheet1
    print("Planilha conectada com sucesso!")
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
