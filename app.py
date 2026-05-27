import os
import requests
from flask import Flask, request

app = Flask(__name__)

# ID da Planilha (O mesmo que você já tem)
SHEET_ID = "1xEzT5SCZRLvcCUSeRTiCQZQZJ4SjtJXTxA_wxQVRUzY"
# URL da API do Google para gravar dados (o "caminho direto")
SHEET_URL = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/Página1!A1:append?valueInputOption=RAW"

@app.route('/')
def home():
    return "Agente de Lenha Otimizado: Online e pronto para o WhatsApp!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == "lenha_agente_secreto_2026":
            return request.args.get('hub.challenge')
        return "Token inválido", 403
    
    # Aqui é onde o WhatsApp envia a mensagem
    data = request.json
    print(data) # Isso vai aparecer nos logs do Render para você ver o que o WhatsApp manda!
    
    return "OK", 200

if __name__ == '__main__':
    app.run()
