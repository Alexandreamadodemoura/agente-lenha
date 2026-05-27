import os
import requests
import google.generativeai as genai
from flask import Flask, request

app = Flask(__name__)

# Configuração
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['GET'])
def home():
    return "ONLINE", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == "lenha_agente_secreto_2026":
            return request.args.get('hub.challenge')
        return "Token inválido", 403
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
