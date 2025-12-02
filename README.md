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
python app.py
```

A aplicação sobe em `http://localhost:5000`.

## Configurações opcionais

- `PLAN_PRICE`, `PLAN_CURRENCY`, `PLAN_REQUESTS`: personalizam o card de preço.
- `MERCADOPAGO_PUBLIC_KEY` e `MERCADOPAGO_ACCESS_TOKEN`: mantenha-os em variáveis de ambiente para configurar o checkout server-side.

## Estrutura

- `app.py`: servidor Flask, rotas da landing page e endpoint demo `/api/consultar`.
- `templates/index.html`: layout principal e JavaScript da demonstração.
- `static/style.css`: estilos visuais.
