from flask import Flask, jsonify, render_template, request
from urllib.parse import quote_plus
import mercadopago
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


@app.route("/api/checkout", methods=["POST"])
def checkout():
    access_token = os.getenv("MERCADOPAGO_ACCESS_TOKEN")
    if not access_token:
        return (
            jsonify(
                {
                    "erro": "Configure a variável de ambiente MERCADOPAGO_ACCESS_TOKEN com seu token de acesso."
                }
            ),
            500,
        )

    sdk = mercadopago.SDK(access_token)
    preference_data = {
        "items": [
            {
                "title": "Assinatura API de Consulta de Veículos",
                "description": "Plano mensal - 60 consultas por minuto, uso ilimitado no mês",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(os.getenv("PLAN_PRICE", 400)),
            }
        ],
        "back_urls": {
            "success": os.getenv("CHECKOUT_SUCCESS_URL", "http://localhost:5000/"),
            "failure": os.getenv("CHECKOUT_FAILURE_URL", "http://localhost:5000/"),
            "pending": os.getenv("CHECKOUT_PENDING_URL", "http://localhost:5000/"),
        },
        "auto_return": "approved",
    }

    payer_email = request.json.get("email") if request.is_json else None
    if payer_email:
        preference_data["payer"] = {"email": payer_email}

    try:
        preference_response = sdk.preference().create(preference_data)
        init_point = preference_response.get("response", {}).get("init_point")
        if not init_point:
            raise ValueError("Resposta do Mercado Pago não contém init_point")
        return jsonify({"checkout_url": init_point})
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"erro": f"Não foi possível criar o checkout: {exc}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
