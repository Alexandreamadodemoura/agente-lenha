from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "O ROBÔ ESTÁ VIVO E ONLINE!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return "OK", 200

if __name__ == '__main__':
    app.run()
