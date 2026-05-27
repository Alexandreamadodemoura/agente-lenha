import os
import requests
from flask import Flask, request

app = Flask(__name__)

# COLE AQUI A URL QUE VOCÊ COPIOU DO GOOGLE APPS SCRIPT
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyd3aqtSw-O09eOs2rFaCM_ZRs1yI3NG_Hfp6bfMTyq3li9SbOc5qlD91CL8aNiFIni/exec"

@app.route('/')
def home():
    return "Robô de Lenha Online e Conectado à Planilha!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    # Simulamos os dados que o Gemini extrairia da foto
    dados = {
        "lugar": "Maringá",
        "data": "26/05/2026",
        "peso": "15000",
        "placa": "ABC-1234",
        "peso_liquido": "14000"
    }
    
    # Envio para a planilha via Apps Script
    try:
        resposta = requests.post(APPS_SCRIPT_URL, json=dados)
        return f"Dados enviados! Resposta do Google: {resposta.text}", 200
    except Exception as e:
        return f"Erro ao enviar: {str(e)}", 500

if __name__ == '__main__':
    app.run()
