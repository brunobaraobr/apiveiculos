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
# opcional: crie um arquivo .env com as variáveis abaixo
cat > .env <<'ENV'
WHATSAPP_NUMBER=5599999999999
WHATSAPP_MESSAGE="Olá! Quero contratar a API de consulta de veículos."
MERCADOPAGO_ACCESS_TOKEN="APP_USR_SEU_TOKEN"
ENV

# ou exporte manualmente
export WHATSAPP_NUMBER=5599999999999
export WHATSAPP_MESSAGE="Olá! Quero contratar a API de consulta de veículos."
export MERCADOPAGO_ACCESS_TOKEN="APP_USR_SEU_TOKEN"
python app.py
```

A aplicação sobe em `http://localhost:5000`.

## Configurações opcionais

- `PLAN_PRICE`, `PLAN_CURRENCY`, `PLAN_REQUESTS`: personalizam o card de preço (padrão `R$ 400` com 60 consultas/min e uso ilimitado no mês).
- `MERCADOPAGO_ACCESS_TOKEN` (ou `MERCADO_PAGO_ACCESS_TOKEN`): token de produção usado para criar a preferência de pagamento via `/api/checkout`. O aplicativo lê automaticamente valores definidos em `.env`.
- `CHECKOUT_SUCCESS_URL`, `CHECKOUT_FAILURE_URL`, `CHECKOUT_PENDING_URL`: URLs para redirecionamento após o pagamento no Mercado Pago.

## Estrutura

- `app.py`: servidor Flask, rotas da landing page e endpoint demo `/api/consultar`.
- `templates/index.html`: layout principal e JavaScript da demonstração.
- `static/style.css`: estilos visuais.
