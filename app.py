import os
import json
import google.generativeai as genai
import gspread
from flask import Flask, request

app = Flask(__name__)

# Configuração Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Configuração Planilha - FORÇANDO A LEITURA DA MEMÓRIA
sheet = None
erro_conexao = "Aguardando..."

try:
    cred_json_str = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if cred_json_str:
        creds_dict = json.loads(cred_json_str)
        # Usamos o método direto que não busca arquivos no disco
        client = gspread.service_account_from_dict(creds_dict)
        sheet = client.open_by_key("1xEzT5SCZRLvcCUSeRTiCQZQZJ4SjtJXTxA_wxQVRUzY").sheet1
    else:
        erro_conexao = "Variável GOOGLE_CREDENTIALS_JSON faltando."
except Exception as e:
    # Mostramos exatamente o que causou o erro
    erro_conexao = f"{type(e).__name__}: {str(e)}"

@app.route('/')
def home():
    if sheet:
        return "Agente de Lenha Ativo! Planilha: CONECTADA COM SUCESSO!", 200
    else:
        return f"Agente de Lenha Ativo! MAS ocorreu um erro: -> {erro_conexao} <-", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return "OK", 200

if __name__ == '__main__':
    app.run()
