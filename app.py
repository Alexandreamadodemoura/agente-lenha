import os
import json
import base64
import requests
import google.generativeai as genai
import gspread
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Configuração Gemini e Planilha
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def extrair_peso_da_foto(image_url, token):
    # Baixa a imagem do WhatsApp
    headers = {"Authorization": f"Bearer {token}"}
    img_data = requests.get(image_url, headers=headers).content
    
    # Pergunta ao Gemini qual é o peso na imagem
    response = model.generate_content([
        "Extraia apenas o valor numérico do peso desta imagem de comprovante. Responda apenas o número.",
        {"mime_type": "image/jpeg", "data": img_data}
    ])
    return response.text.strip()

# [Configuração da Planilha - A mesma que já tínhamos]
# (Cole aqui o seu trecho de conexão com o gspread que já estava funcionando)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == "lenha_agente_secreto_2026":
            return request.args.get('hub.challenge')
        return "Token inválido", 403

    data = request.json
    # Verifica se é uma mensagem de imagem
    if 'messages' in data['entry'][0]['changes'][0]['value']:
        msg = data['entry'][0]['changes'][0]['value']['messages'][0]
        if 'image' in msg:
            img_id = msg['image']['id']
            # Pega o link da imagem (precisa da API do WhatsApp para pegar o link real)
            # ... (Lógica para obter o link via Graph API da Meta)
            peso = extrair_peso_da_foto(link_da_imagem, "SEU_TOKEN_WHATSAPP")
            sheet.append_row(["Data", "Motorista", peso])
            
    return "OK", 200
