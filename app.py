from flask import Flask, jsonify, render_template, request
from urllib.parse import quote_plus
import os

app = Flask(__name__)

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
        "value": os.getenv("PLAN_PRICE", "39,90"),
        "currency": os.getenv("PLAN_CURRENCY", "R$"),
        "requests": os.getenv("PLAN_REQUESTS", "500"),
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
