# RecargaPay PIX API

API de automação de pagamentos PIX via RecargaPay, construída com **FastAPI** e pronta para deploy no **Railway**.

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET`  | `/` | Boas-vindas e mapa de endpoints |
| `GET`  | `/health` | Health check (Railway) |
| `GET`  | `/status` | Status de todos os tokens |
| `POST` | `/status/renew` | Renovar Bearer Token manualmente |
| `POST` | `/pix/key` | Pagar PIX por chave (CPF/CNPJ/PHONE/EMAIL/EVP) |
| `POST` | `/pix/contact` | Pagar PIX por contato recente |
| `GET`  | `/pix/history` | Histórico de transações |
| `GET`  | `/pix/contacts` | Listar contatos recentes |
| `GET`  | `/pix/keys` | Listar chaves PIX da conta |
| `GET`  | `/pix/balance` | Consultar saldo da carteira |
| `POST` | `/pix/lookup` | Consultar destinatário sem pagar |
| `GET`  | `/pix/integrity-hash` | Gerar integrityHash para uma chave |
| `GET`  | `/docs` | Swagger UI (documentação interativa) |
| `GET`  | `/redoc` | ReDoc |

## Deploy no Railway

1. Acesse [railway.app](https://railway.app) e crie um novo projeto
2. Selecione **"Deploy from GitHub repo"** e escolha este repositório
3. Em **Settings > Variables**, adicione as variáveis do `.env.example`
4. O Railway detecta automaticamente o `railway.toml` e faz o build

## Variáveis de Ambiente Obrigatórias

| Variável | Descrição |
|----------|-----------|
| `GOOGLE_REFRESH_TOKEN` | Token permanente Google OAuth2 (renovação automática do Bearer) |
| `BEARER_TOKEN` | Bearer Token RecargaPay atual |
| `PIN_CODE` | PIN de segurança da conta |

As demais variáveis já têm valores padrão extraídos do APK/HAR.

## Exemplo de uso

```bash
# Pagar R$ 10,00 por CPF
curl -X POST https://sua-api.railway.app/pix/key \
  -H "Content-Type: application/json" \
  -d '{"key_type": "CPF", "key_value": "55537568802", "amount": "10.00"}'

# Verificar status dos tokens
curl https://sua-api.railway.app/status
```

## Renovação Automática de Tokens

A API renova o Bearer Token automaticamente em 2 etapas:
1. **Google OAuth2**: `GOOGLE_REFRESH_TOKEN` → novo `access_token` (sem `client_secret`)
2. **RecargaPay login**: `grant_type=google_access_token` → novo Bearer Token (~24h)

Nenhuma intervenção manual é necessária enquanto o `GOOGLE_REFRESH_TOKEN` estiver válido.
