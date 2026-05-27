import os
import requests
import google.generativeai as genai
from flask import Flask, request

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Cole aqui a URL que o Google Apps Script lhe deu
APPS_SCRIPT_URL = "COLE_A_SUA_URL_AQUI"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Lógica simplificada: aqui você extrairia a imagem do WhatsApp
    # e chamaria o Gemini:
    # response = model.generate_content(["Extraia: lugar, data, peso, placa, peso liquido", imagem])
    
    # Exemplo de como enviar para a planilha:
    payload = {
        "lugar_entregue": "Maringá",
        "data": "26/05/2026",
        "peso": "12000",
        "placa": "ABC-1234",
        "peso_liquido": "11500"
    }
    requests.post(APPS_SCRIPT_URL, json=payload)
    
    return "OK", 200

if __name__ == '__main__':
    app.run()
