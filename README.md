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
DEMO_API_KEY="chave-demo"
RATE_LIMIT_REQUESTS=20
RATE_LIMIT_WINDOW=60
ENV

# ou exporte manualmente
export WHATSAPP_NUMBER=5599999999999
export WHATSAPP_MESSAGE="Olá! Quero contratar a API de consulta de veículos."
export DEMO_API_KEY="chave-demo"
export RATE_LIMIT_REQUESTS=20
export RATE_LIMIT_WINDOW=60
python app.py
```

A aplicação sobe em `http://localhost:5000`.

## Configurações opcionais

- `PLAN_PRICE`, `PLAN_CURRENCY`, `PLAN_REQUESTS`: personalizam o card de preço (padrão `R$ 400` com 60 consultas/min e uso ilimitado no mês).
- `DEMO_API_KEY`: se definido, toda consulta ao endpoint `/api/consultar` deve conter a chave em `X-API-KEY` ou no corpo `api_key`.
- `RATE_LIMIT_REQUESTS` e `RATE_LIMIT_WINDOW`: controlam o número máximo de consultas por IP dentro da janela (por padrão, 20 solicitações em 60 segundos).

## Estrutura

- `app.py`: servidor Flask, rotas da landing page e endpoint demo `/api/consultar`.
- `templates/index.html`: layout principal e JavaScript da demonstração.
- `static/style.css`: estilos visuais.
