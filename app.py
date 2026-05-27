import os
import requests
import google.generativeai as genai
from flask import Flask, request

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby426xVIij60vcry6U4cRrLKwS0GiVM2cnbGKPlerlnOdofXVoKj7j-TG5HIi1fUg5c/exec" # Cole aqui aquele link que termina em /exec

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # 1. Validação da Meta (O "Handshake")
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == "lenha_agente_secreto_2026":
            return request.args.get('hub.challenge')
        return "Token inválido", 403

    # 2. Processamento da Mensagem
    if request.method == 'POST':
        data = request.json
        try:
            # Verifica se é uma imagem
            msg = data['entry'][0]['changes'][0]['value']['messages'][0]
            if msg.get('type') == 'image':
                # Aqui entra a lógica: 
                # 1. Baixar imagem via API do WhatsApp
                # 2. Enviar para o Gemini extrair os campos
                # 3. Enviar para a planilha
                print("Imagem recebida com sucesso!")
        except:
            pass
        return "OK", 200

if __name__ == '__main__':
    app.run()
