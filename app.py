import os
import requests
import google.generativeai as genai
from flask import Flask, request

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# URL do seu Google Apps Script (aquele que criámos agora)
APPS_SCRIPT_URL = "SUA_URL_DO_GOOGLE_APPS_SCRIPT_AQUI"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    try:
        # Aqui o seu robô recebe a foto do WhatsApp
        # 1. Obter a imagem (via API do WhatsApp)
        # 2. Enviar ao Gemini:
        instrucao = """
        Analise esta imagem de pesagem de lenha. Extraia estritamente estes 5 campos:
        - Lugar entregue
        - Data
        - Peso bruto
        - Placa do veículo
        - Peso líquido
        Responda apenas em formato JSON, exemplo:
        {"lugar_entregue": "Maringá", "data": "26/05/2026", "peso": "12000", "placa": "ABC-1234", "peso_liquido": "11500"}
        """
        
        # O Gemini processa a imagem (você adicionará a lógica da foto aqui)
        # resposta_gemini = model.generate_content([instrucao, imagem_baixada])
        
        # Exemplo do que será enviado à sua planilha:
        payload = {"lugar_entregue": "Maringá", "data": "26/05/2026", "peso": "12000", "placa": "ABC-1234", "peso_liquido": "11500"}
        
        # Envio automático via rede para o Apps Script
        requests.post(APPS_SCRIPT_URL, json=payload)
        
    except Exception as e:
        print(f"Erro no processamento: {e}")
    
    return "OK", 200

if __name__ == '__main__':
    app.run()
