import os
import requests
import google.generativeai as genai
import gspread
from flask import Flask, request

app = Flask(__name__)

# Configuração do Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Configuração da Planilha e captura de erro
sheet = None
erro_conexao = "Nenhum erro inicial."

try:
    caminho_arquivo = '/etc/secrets/credentials.json'
    client = gspread.service_account(filename=caminho_arquivo)
    sheet = client.open_by_key("1xEzT5SCZRLvcCUSeRTiCQZQZJ4SjtJXTxA_wxQVRUzY").sheet1
except Exception as e:
    # repr() força a exibição da classe e dos detalhes brutos do erro
    erro_conexao = repr(e)
    print(f"Erro capturado: {erro_conexao}")

@app.route('/')
def home():
    if sheet:
        return "Agente de Lenha Ativo! Planilha: CONECTADA COM SUCESSO!", 200
    else:
        # Coloquei setas para destacar exatamente onde o erro deve aparecer
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
