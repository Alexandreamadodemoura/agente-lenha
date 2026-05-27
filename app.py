import os
import requests
import google.generativeai as genai
from flask import Flask, request

app = Flask(__name__)

# Configurações do Gemini (Certifique-se de ter essa variável no Render)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# CONFIGURAÇÕES (Preencha aqui ou via Environment Variables no Render)
APPS_SCRIPT_URL = "SUA_URL_DO_APPS_SCRIPT_AQUI"
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
VERIFY_TOKEN = "lenha_agente_secreto_2026"

@app.route('/', methods=['GET'])
def home():
    return "CONTABILIDADE DE LENHA ATIVA E ESCUTANDO!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # 1. Handshake com a Meta
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Token inválido", 403

    # 2. Processamento da Mensagem (Webhook da Meta)
    if request.method == 'POST':
        data = request.json
        print(f"DEBUG_META_DATA: {data}") # Importante para ver nos logs do Render

        try:
            # Extração segura dos dados
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            
            if 'messages' in value:
                message = value['messages'][0]
                
                # Se for imagem, processa
                if message['type'] == 'image':
                    image_id = message['image']['id']
                    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
                    
                    # Busca URL da imagem na Meta
                    r = requests.get(f"https://graph.facebook.com/v18.0/{image_id}", headers=headers)
                    image_url = r.json()['url']
                    
                    # Baixa o conteúdo
                    img_resp = requests.get(image_url, headers=headers)
                    
                    # Gemini analisa
                    prompt = "Extraia: Lugar, Data, Peso bruto, Placa, Peso líquido. Responda apenas em formato JSON."
                    response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": img_resp.content}])
                    
                    # Envio para Planilha
                    json_text = response.text.replace('```json', '').replace('```', '').strip()
                    requests.post(APPS_SCRIPT_URL, data=json_text)
                    print("PROCESSO CONCLUÍDO: Dados enviados para planilha.")

        except Exception as e:
            print(f"ERRO NO PROCESSAMENTO: {e}")
            
        return "OK", 200

if __name__ == '__main__':
    # O Render exige escuta na porta 10000
    app.run(host='0.0.0.0', port=10000)
