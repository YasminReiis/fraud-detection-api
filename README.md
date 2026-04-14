# 🚨 Real-Time Fraud Detection API

API de detecção de fraude em tempo real desenvolvida com foco em arquitetura de backend profissional.

🔗 API Online:  
https://fraud-detection-api-jvwk.onrender.com

📄 Documentação (Swagger):  
https://fraud-detection-api-jvwk.onrender.com/docs

---

## 💡 Sobre o Projeto

Este projeto simula como sistemas financeiros analisam transações bancárias para detectar possíveis fraudes em tempo real.

A aplicação foi construída utilizando boas práticas de desenvolvimento backend, incluindo autenticação, versionamento de API e tratamento de erros.

---

## 🚀 Funcionalidades

- 🔐 Autenticação com JWT
- 💳 Análise de transações em tempo real
- 🚨 Detecção de fraude baseada em regras
- 📊 Consulta de status por usuário
- 🧠 Lógica inspirada em Machine Learning
- 🛠️ Tratamento global de erros
- ❤️ Health check para monitoramento
- 🔄 Versionamento de API (/v1)

---

## 🧱 Tecnologias Utilizadas

- Python
- FastAPI
- Uvicorn
- PyJWT
- Render (deploy em cloud)

---

## 🔐 Como Funciona a Autenticação

1. O usuário faz login no endpoint:
   POST /v1/auth/login


2. A API retorna um token JWT:

```json
{
  "token": "seu_token_aqui"
}
Esse token deve ser enviado nos endpoints protegidos via header:
authorization: seu_token_aqui
