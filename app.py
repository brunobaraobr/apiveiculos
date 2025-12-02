from collections import defaultdict, deque
from flask import Flask, jsonify, render_template, request
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os
import time

load_dotenv()

app = Flask(__name__)

RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "20"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # segundos
_rate_limits = defaultdict(deque)

SAMPLE_DATA = {
    "ABC1D23": {
        "placa": "ABC1D23",
        "modelo": "Corolla XEi",
        "marca": "Toyota",
        "cidade": "São Paulo",
        "tipo": "Sedan",
        "estado": "SP",
        "cor": "Prata"
    },
    "XYZ9Z88": {
        "placa": "XYZ9Z88",
        "modelo": "Compass Longitude",
        "marca": "Jeep",
        "cidade": "Curitiba",
        "tipo": "SUV",
        "estado": "PR",
        "cor": "Branco"
    },
}


@app.route("/")
def index():
    whatsapp_number = os.getenv("WHATSAPP_NUMBER", "5599999999999")
    whatsapp_message = os.getenv(
        "WHATSAPP_MESSAGE",
        "Olá! Quero contratar a API de consulta de veículos."
    )
    whatsapp_link = build_whatsapp_link(whatsapp_number, whatsapp_message)

    pricing = {
        "value": os.getenv("PLAN_PRICE", "400"),
        "currency": os.getenv("PLAN_CURRENCY", "R$"),
        "requests": os.getenv(
            "PLAN_REQUESTS",
            "60 consultas/min • uso ilimitado mensal",
        ),
    }

    return render_template(
        "index.html",
        whatsapp_link=whatsapp_link,
        whatsapp_message=whatsapp_message,
        pricing=pricing,
    )


def build_whatsapp_link(number: str, message: str) -> str:
    digits_only = "".join(filter(str.isdigit, number))
    return f"https://wa.me/{digits_only}?text={quote_plus(message)}"


@app.route("/api/consultar", methods=["POST"])
def consultar():
    payload = request.get_json(silent=True) or {}
    api_key = payload.get("api_key") or request.headers.get("X-API-KEY")
    expected_key = (os.getenv("DEMO_API_KEY") or "").strip()

    if expected_key and api_key != expected_key:
        return jsonify({"erro": "Acesso não autorizado."}), 401

    client_ip = _get_client_ip()
    if _is_rate_limited(client_ip):
        return jsonify({"erro": "Limite de consultas temporariamente excedido. Aguarde um instante."}), 429

    plate = (payload.get("placa") or "").strip().upper()

    if not plate:
        return jsonify({"erro": "Informe uma placa para consultar."}), 400

    data = SAMPLE_DATA.get(plate) or {
        "placa": plate,
        "modelo": "N/D",
        "marca": "N/D",
        "cidade": "N/D",
        "tipo": "N/D",
        "estado": "N/D",
        "cor": "N/D",
        "observacao": "Placa não encontrada na base demonstrativa."
    }

    return jsonify(data)


def _get_client_ip() -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.remote_addr or "unknown"


def _is_rate_limited(client_ip: str) -> bool:
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW
    bucket = _rate_limits[client_ip]

    while bucket and bucket[0] < window_start:
        bucket.popleft()

    if len(bucket) >= RATE_LIMIT_REQUESTS:
        return True

    bucket.append(now)
    return False


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
