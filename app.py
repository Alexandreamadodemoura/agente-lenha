import os
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# COLOQUE SEU LINK DO GOOGLE AQUI (O que termina em /exec)
APPS_SCRIPT_URL ="https://script.google.com/macros/s/AKfycby426xVIij60vcry6U4cRrLKwS0GiVM2cnbGKPlerlnOdofXVoKj7j-TG5HIi1fUg5c/exec"
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
VERIFY_TOKEN = "lenha_agente_secreto_2026"

@app.route('/')
def home():
    return "CONTABILIDADE DE LENHA ATIVA!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # Validação da Meta
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Token inválido", 403

    # Processamento da Mensagem (POST)
    data = request.json
    try:
        if 'messages' in data['entry'][0]['changes'][0]['value']:
            message = data['entry'][0]['changes'][0]['value']['messages'][0]
            phone_number = message['from']
            
            if message['type'] == 'image':
                image_id = message['image']['id']
                
                # 1. Obter URL da imagem na Meta
                headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
                media_url_info = requests.get(f"https://graph.facebook.com/v18.0/{image_id}", headers=headers).json()
                image_url = media_url_info['url']
                
                # 2. Baixar a imagem
                image_data = requests.get(image_url, headers=headers).content
                
                # 3. Gemini processa a imagem
                prompt = """Analise esta imagem de pesagem. Extraia exatamente estes campos:
                Lugar entregue, Data, Peso bruto, Placa, Peso líquido.
                Responda APENAS em JSON, assim:
                {"lugar": "texto", "data": "texto", "peso": "texto", "placa": "texto", "peso_liquido": "texto"}"""
                
                response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_data}])
                # Limpa a resposta para garantir que seja apenas JSON
                json_data = response.text.replace('```json', '').replace('```', '').strip()
                
                # 4. Enviar para a Planilha (Apps Script)
                requests.post(APPS_SCRIPT_URL, data=json_data)
                
                # 5. Opcional: Responder ao usuário (Se quiser configurar o envio de volta)
                print(f"Sucesso! Dados salvos para o número {phone_number}")

    except Exception as e:
        print(f"Erro no processamento: {str(e)}")

    return "OK", 200

if __name__ == '__main__':
    app.run()
