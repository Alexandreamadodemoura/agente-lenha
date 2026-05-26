import os
import json
import google.generativeai as genai
import gspread
from flask import Flask, request

app = Flask(__name__)

# Configuração Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Configuração Planilha
sheet = None
erro_conexao = "Aguardando conexão..."

try:
    # Lemos a string da variável de ambiente
    cred_json_str = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if cred_json_str:
        # Carrega o JSON da string e autoriza
        creds_dict = json.loads(cred_json_str)
        client = gspread.service_account_from_dict(creds_dict)
        sheet = client.open_by_key("1xEzT5SCZRLvcCUSeRTiCQZQZJ4SjtJXTxA_wxQVRUzY").sheet1
    else:
        erro_conexao = "Variável GOOGLE_CREDENTIALS_JSON não encontrada."
except Exception as e:
    erro_conexao = repr(e)

@app.route('/')
def home():
    if sheet:
        return "Agente de Lenha Ativo! Planilha: CONECTADA COM SUCESSO!", 200
    else:
        return f"Agente de Lenha Ativo! MAS ocorreu um erro: -> {erro_conexao} <-", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == "lenha_agente_secreto_2026":
            return request.args.get('hub.challenge')
        return "Token inválido", 403
    return "OK", 200

if __name__ == '__main__':
    app.run()
