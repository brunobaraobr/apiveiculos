# API de Consulta de Veículos

Landing page em Flask para divulgar e vender uma API de consulta de veículos por placa.

## Requisitos

- Python 3.11+
- Dependências do `requirements.txt`

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export WHATSAPP_NUMBER=5599999999999
export WHATSAPP_MESSAGE="Olá! Quero contratar a API de consulta de veículos."
export MERCADOPAGO_ACCESS_TOKEN="seu_token_mercado_pago"
python app.py
```

A aplicação sobe em `http://localhost:5000`.

## Configurações opcionais

- `PLAN_PRICE`, `PLAN_CURRENCY`, `PLAN_REQUESTS`: personalizam o card de preço (padrão `R$ 400` com 60 consultas/min e uso ilimitado no mês).
- `MERCADOPAGO_ACCESS_TOKEN` (ou `MERCADO_PAGO_ACCESS_TOKEN`): token de produção usado para criar a preferência de pagamento via `/api/checkout`.
- `CHECKOUT_SUCCESS_URL`, `CHECKOUT_FAILURE_URL`, `CHECKOUT_PENDING_URL`: URLs para redirecionamento após o pagamento no Mercado Pago.

## Estrutura

- `app.py`: servidor Flask, rotas da landing page e endpoint demo `/api/consultar`.
- `templates/index.html`: layout principal e JavaScript da demonstração.
- `static/style.css`: estilos visuais.
