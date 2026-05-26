import os
import json
import requests
import google.generativeai as genai
import gspread
from flask import Flask, request

app = Flask(__name__)

# Configuração do Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Configuração da Planilha na Memória
sheet = None
erro_conexao = "Nenhum erro inicial."

try:
    # Lemos o texto puro direto da variável de ambiente que você acabou de criar
    credenciais_texto = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    
    if credenciais_texto:
        # Converte o texto para um dicionário que o gspread entende
        credenciais_dict = json.loads(credenciais_texto)
        client = gspread.service_account_from_dict(credenciais_dict)
        sheet = client.open_by_key("1xEzT5SCZRLvcCUSeRTiCQZQZJ4SjtJXTxA_wxQVRUzY").sheet1
    else:
        erro_conexao = "A variável GOOGLE_CREDENTIALS_JSON não foi encontrada no Render."
        
except Exception as e:
    # Se algo der errado, capturamos o erro técnico
    erro_conexao = repr(e)
    print(f"Erro capturado: {erro_conexao}")

@app.route('/')
def home():
    if sheet:
        return "Agente de Lenha Ativo! Planilha: CONECTADA COM SUCESSO!", 200
    else:
        return f"Agente de Lenha Ativo! MAS ocorreu um erro com a Planilha: -> {erro_conexao} <-", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == "lenha_agente_secreto_2026":
            return request.args.get('hub.challenge')
        return "Token inválido", 403
    
    return "OK", 200

if __name__ == '__main__':
    app.run()
