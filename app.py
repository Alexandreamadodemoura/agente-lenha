import os
import requests
import google.generativeai as genai
from flask import Flask, request

app = Flask(__name__)

# Configurações do ambiente
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

APPS_SCRIPT_URL = "SUA_URL_DO_APPS_SCRIPT_AQUI" # Cole aqui sua URL
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
VERIFY_TOKEN = "lenha_agente_secreto_2026"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Token inválido", 403

    if request.method == 'POST':
        data = request.json
        try:
            value = data['entry'][0]['changes'][0]['value']
            if 'messages' in value:
                message = value['messages'][0]
                
                # Processamento de imagem
                if message['type'] == 'image':
                    image_id = message['image']['id']
                    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
                    
                    # Obter URL e baixar imagem
                    url_data = requests.get(f"https://graph.facebook.com/v18.0/{image_id}", headers=headers).json()
                    image_content = requests.get(url_data['url'], headers=headers).content
                    
                    # Gemini analisa
                    prompt = "Extraia: Lugar, Data, Peso bruto, Placa, Peso líquido. Responda apenas em JSON."
                    response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_content}])
                    
                    # Envia para a planilha
                    requests.post(APPS_SCRIPT_URL, data=response.text.replace('```json', '').replace('
```', '').strip())
                    print("Dados enviados com sucesso!")
        except Exception as e:
            print(f"Erro: {e}")
        return "OK", 200

if __name__ == '__main__':
    app.run()
