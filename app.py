from flask import Flask, request, jsonify

app = Flask(__name__)
from flask import Flask, request, jsonify
# ... (outros imports se houver)

app = Flask(__name__)

# --- ADICIONE ESSAS 3 LINHAS AQUI ---
@app.route('/')
def home():
    return "Servidor do Agente de Lenha Ativo!", 200
# -------------------------------------

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # ... resto do seu código que já estava aí ...
# Esse token é uma "senha" que nós inventamos. 
# Guarde ela, pois vamos digitar essa MESMA senha lá no painel da Meta para ativar a conexão.
VERIFY_TOKEN = "lenha_agente_secreto_2026"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # 1. VALIDAÇÃO DA META (Acontece apenas uma vez, quando ativamos o robô no painel)
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print("✅ Webhook validado e conectado com sucesso à Meta!")
                return challenge, 200
            else:
                return "Token de verificação incorreto", 403
                
    # 2. RECEBIMENTO DE DADOS (Aqui chegarão os textos e fotos enviados pelos motoristas)
    elif request.method == 'POST':
        dados = request.json
        
        # Exibe na tela preta tudo o que o WhatsApp enviar, em tempo real
        print("\n📩 Nova notificação recebida do WhatsApp:")
        print(dados)
        
        # Avisa a Meta que a mensagem foi recebida com sucesso pelo nosso computador
        return jsonify({"status": "sucesso"}), 200

if __name__ == '__main__':
    # Roda o servidor localmente na porta 5000
    app.run(port=5000)
