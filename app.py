import os
import requests
import google.generativeai as genai
from flask import Flask, request

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Cole o link do seu Google Apps Script abaixo:
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyd3aqtSw-O09eOs2rFaCM_ZRs1yI3NG_Hfp6bfMTyq3li9SbOc5qlD91CL8aNiFIni/exec"
VERIFY_TOKEN = "lenha_agente_secreto_2026"

@app.route('/', methods=['GET'])
def home():
    return "CONTABILIDADE DE LENHA ATIVA!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # 1. Validação da Meta (O "Handshake")
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Token inválido", 403

    # 2. Processamento da Mensagem (POST)
    if request.method == 'POST':
        data = request.json
        print(f"DADOS RECEBIDOS: {data}") # Isso aparecerá nos logs do Render
        
        try:
            # Verifica se é uma imagem
            entry = data.get('entry', [])[0]
            change = entry.get('changes', [])[0]
            value = change.get('value', {})
            messages = value.get('messages', [])
            
            if messages and messages[0].get('type') == 'image':
                print("Imagem detectada! O robô vai processar agora.")
                # (A lógica de extração do Gemini entra aqui no próximo passo)
                
        except Exception as e:
            print(f"Erro ao processar: {e}")
            
        return "OK", 200

if __name__ == '__main__':
    app.run()
