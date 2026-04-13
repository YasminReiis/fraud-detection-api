from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(
    title="🚨 Real-Time Fraud Detection API",
    description="""
Sistema de detecção de fraude em tempo real.

Essa API simula análise de transações bancárias utilizando regras simples
e lógica inspirada em machine learning.

Funcionalidades:
- Analisar transações
- Detectar possíveis fraudes
- Consultar status por usuário

Tecnologias:
- FastAPI
- Python
- Deploy em Cloud (Render)
""",
    version="1.0.0"
)

# "banco" simples (memória)
fake_db = {}

class Transaction(BaseModel):
    user_id: int
    amount: float
    location: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "amount": 2500,
                "location": "US"
            }
        }

# página inicial (remove erro Not Found)
@app.get("/")
def home():
    return {
        "message": "🚀 Fraud Detection API está online",
        "docs": "/docs"
    }

# lógica simples de fraude
def predict_fraud(transaction):
    score = 0

    if transaction["amount"] > 1000:
        score += 1

    if transaction["location"] != "BR":
        score += 1

    if random.random() > 0.7:
        score += 1

    return "FRAUDE" if score >= 2 else "OK"

# endpoint principal (melhorado)
@app.post("/transactions/analyze", summary="Analisar transação para possível fraude")
def analyze_transaction(tx: Transaction):
    status = predict_fraud(tx.dict())

    fake_db[tx.user_id] = status

    return {
        "user_id": tx.user_id,
        "amount": tx.amount,
        "status": status,
        "message": "Transação analisada com sucesso"
    }

# endpoint de consulta (melhorado)
@app.get("/transactions/{user_id}/status", summary="Consultar status da transação")
def get_status(user_id: int):
    status = fake_db.get(user_id, "Sem dados")

    return {
        "user_id": user_id,
        "status": status
    }
