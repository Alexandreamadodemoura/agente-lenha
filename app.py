import os
import requests
import google.generativeai as genai
from flask import Flask, request

app = Flask(__name__)

# Configuração Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# ID da Planilha (Mantenha o mesmo)
SHEET_ID = "1xEzT5SCZRLvcCUSeRTiCQZQZJ4SjtJXTxA_wxQVRUzY"

@app.route('/')
def home():
    return "Agente de Lenha Otimizado: Online e pronto para o WhatsApp!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # Validação do Webhook do WhatsApp
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == "lenha_agente_secreto_2026":
            return request.args.get('hub.challenge')
        return "Token inválido", 403
    
    # Aqui processaremos as mensagens futuramente
    return "OK", 200

if __name__ == '__main__':
    app.run()
