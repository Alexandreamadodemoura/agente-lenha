import os
import requests
from flask import Flask, request

app = Flask(__name__)

# COLE AQUI A URL QUE VOCÊ COPIOU NO PASSO 1
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby426xVIij60vcry6U4cRrLKwS0GiVM2cnbGKPlerlnOdofXVoKj7j-TG5HIi1fUg5c/exec"

@app.route('/')
def home():
    return "Robô ativo e pronto para enviar dados!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    # Aqui vamos simular o envio dos dados (após extrair da foto)
    dados = {
        "lugar": "Maringá",
        "data": "26/05/2026",
        "peso": "15000",
        "placa": "ABC-1234",
        "peso_liquido": "14000"
    }
    # O robô envia os dados para a planilha sem precisar de permissões especiais!
    requests.post(APPS_SCRIPT_URL, json=dados)
    return "Dados enviados!", 200

if __name__ == '__main__':
    app.run()
