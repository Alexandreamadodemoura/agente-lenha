import os
import requests
import json
import google.generativeai as genai
from flask import Flask, request

app = Flask(__name__)

# ── Configuração ──────────────────────────────────────────────────────────────
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

WHATSAPP_TOKEN   = os.environ.get("WHATSAPP_TOKEN")
VERIFY_TOKEN     = "lenha_agente_secreto_2026"
SHEETS_WEBHOOK   = os.environ.get("SHEETS_WEBHOOK_URL")   # URL /exec do Apps Script


# ── Rota de saúde ─────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return "ONLINE", 200


# ── Webhook principal ─────────────────────────────────────────────────────────
@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # Verificação do webhook pela Meta
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Token inválido", 403

    # Recepção de mensagens
    if request.method == "POST":
        try:
            body = request.get_json()
            entry = body["entry"][0]["changes"][0]["value"]

            # Ignorar notificações de status (delivered, read, etc.)
            if "messages" not in entry:
                return "OK", 200

            mensagem = entry["messages"][0]
            numero   = mensagem["from"]

            # ── Mensagem de IMAGEM ────────────────────────────────────────────
            if mensagem["type"] == "image":
                image_id = mensagem["image"]["id"]
                processar_ticket(numero, image_id)

            # ── Mensagem de TEXTO ─────────────────────────────────────────────
            elif mensagem["type"] == "text":
                texto = mensagem["text"]["body"].strip().lower()
                if texto in ["oi", "olá", "ola", "bom dia", "boa tarde"]:
                    enviar_mensagem(numero,
                        "Olá! 👋 Sou o agente de contabilidade de lenha.\n"
                        "Envie a foto do tíquete de pesagem e vou registrar os dados automaticamente. 🌲")
                else:
                    enviar_mensagem(numero,
                        "Por favor, envie a *foto do tíquete de pesagem* para eu registrar. 📷")

        except Exception as e:
            print(f"[ERRO webhook] {e}")

        return "OK", 200


# ── Processamento do tíquete ──────────────────────────────────────────────────
def processar_ticket(numero: str, image_id: str):
    """Baixa a imagem, extrai dados com Gemini e grava no Sheets."""

    # 1. Obter URL da imagem via API do WhatsApp
    url_info = f"https://graph.facebook.com/v19.0/{image_id}"
    headers  = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    resp     = requests.get(url_info, headers=headers, timeout=15)
    image_url = resp.json().get("url")

    if not image_url:
        enviar_mensagem(numero, "❌ Não consegui acessar a imagem. Tente reenviar.")
        return

    # 2. Baixar o conteúdo binário da imagem
    img_resp = requests.get(image_url, headers=headers, timeout=20)
    if img_resp.status_code != 200:
        enviar_mensagem(numero, "❌ Erro ao baixar a imagem. Tente novamente.")
        return

    image_bytes = img_resp.content

    # 3. Enviar para o Gemini e extrair dados do tíquete
    prompt = """
    Analise este tíquete de pesagem de lenha e extraia as seguintes informações.
    Responda APENAS com um objeto JSON válido, sem markdown, sem texto adicional.

    Campos obrigatórios:
    {
      "motorista": "nome completo do motorista ou 'Não informado'",
      "placa": "placa do veículo ou 'Não informado'",
      "data_ticket": "data no formato DD/MM/AAAA ou 'Não informado'",
      "hora_ticket": "hora no formato HH:MM ou 'Não informado'",
      "peso_bruto": "peso bruto em kg (apenas número) ou 0",
      "peso_tara": "peso tara em kg (apenas número) ou 0",
      "peso_liquido": "peso líquido em kg (apenas número) ou 0",
      "produto": "tipo de produto (ex: Lenha Eucalipto) ou 'Lenha'",
      "fornecedor": "nome do fornecedor/origem ou 'Não informado'",
      "numero_ticket": "número do tíquete ou 'Não informado'"
    }
    """

    try:
        import PIL.Image
        import io
        imagem_pil = PIL.Image.open(io.BytesIO(image_bytes))
        resposta   = model.generate_content([prompt, imagem_pil])
        texto_json = resposta.text.strip()

        # Limpar possível markdown do Gemini
        if texto_json.startswith("```"):
            texto_json = texto_json.split("```")[1]
            if texto_json.startswith("json"):
                texto_json = texto_json[4:]
            texto_json = texto_json.strip()

        dados = json.loads(texto_json)

    except json.JSONDecodeError as e:
        print(f"[ERRO Gemini JSON] {e} | Resposta: {texto_json}")
        enviar_mensagem(numero,
            "⚠️ Consegui ler a imagem mas não identifiquei um tíquete válido.\n"
            "Certifique-se de enviar a foto do tíquete de pesagem.")
        return
    except Exception as e:
        print(f"[ERRO Gemini] {e}")
        enviar_mensagem(numero, "❌ Erro ao processar a imagem com IA. Tente novamente.")
        return

    # 4. Gravar no Google Sheets via Apps Script
    dados["numero_whatsapp"] = numero
    sucesso = enviar_para_sheets(dados)

    # 5. Confirmar para o usuário
    if sucesso:
        peso_liq = dados.get("peso_liquido", 0)
        placa    = dados.get("placa", "N/A")
        data_tk  = dados.get("data_ticket", "N/A")
        num_tk   = dados.get("numero_ticket", "N/A")

        msg = (
            f"✅ *Tíquete registrado com sucesso!*\n\n"
            f"🎫 Ticket nº: {num_tk}\n"
            f"📅 Data: {data_tk}\n"
            f"🚛 Placa: {placa}\n"
            f"⚖️ Peso líquido: *{peso_liq} kg*\n\n"
            f"Dados gravados na planilha. 📊"
        )
    else:
        msg = (
            "⚠️ Imagem processada, mas houve erro ao gravar na planilha.\n"
            "Avise o administrador para verificar o Google Sheets."
        )

    enviar_mensagem(numero, msg)


# ── Envio para Google Sheets ──────────────────────────────────────────────────
def enviar_para_sheets(dados: dict) -> bool:
    """Envia os dados extraídos para o Google Apps Script."""
    if not SHEETS_WEBHOOK:
        print("[ERRO] SHEETS_WEBHOOK_URL não configurada nas variáveis de ambiente.")
        return False

    try:
        resp = requests.post(
            SHEETS_WEBHOOK,
            data=json.dumps(dados),          # data= (não json=) para Apps Script
            headers={"Content-Type": "application/json"},
            timeout=30,
            allow_redirects=True             # Essencial — o Google faz redirect
        )
        resultado = resp.json()
        print(f"[Sheets] Resposta: {resultado}")
        return resultado.get("status") == "ok"

    except Exception as e:
        print(f"[ERRO Sheets] {e}")
        return False


# ── Envio de mensagem WhatsApp ────────────────────────────────────────────────
def enviar_mensagem(numero: str, texto: str):
    """Envia mensagem de texto via WhatsApp Cloud API."""
    phone_number_id = os.environ.get("PHONE_NUMBER_ID")
    if not phone_number_id:
        print("[ERRO] PHONE_NUMBER_ID não configurado.")
        return

    url     = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type":  "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to":   numero,
        "type": "text",
        "text": {"body": texto},
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"[WhatsApp] Status {resp.status_code} → {numero}")
    except Exception as e:
        print(f"[ERRO WhatsApp] {e}")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
