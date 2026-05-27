from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "O ROBÔ ESTÁ VIVO E ONLINE!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # Isso é o que a Meta usa para verificar seu servidor
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == "lenha_agente_secreto_2026":
            return request.args.get('hub.challenge')
        return "Token inválido", 403
    
    # Isso é o que recebe as mensagens depois de validado
    if request.method == 'POST':
        return "OK", 200

if __name__ == '__main__':
    app.run()
