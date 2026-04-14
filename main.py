from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import random
import jwt

# segredo simples (depois dá pra melhorar)
SECRET = "meu_segredo_super"

app = FastAPI(
    title="🚨 Real-Time Fraud Detection API",
    description="""
Sistema de detecção de fraude em tempo real.

Funcionalidades:
- Login com token (JWT)
- Análise de transações
- Detecção de fraude
- Consulta de status
""",
    version="1.1.0"
)

# "banco" simples
fake_db = {}

# modelo da transação
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

# rota inicial
@app.get("/")
def home():
    return {
        "name": "Fraud Detection API",
        "status": "online",
        "version": "1.1.0",
        "docs": "/docs"
    }

# LOGIN (gera token)
@app.post("/login", summary="Gerar token de acesso")
def login():
    token = jwt.encode({"user_id": 1}, SECRET, algorithm="HS256")
    return {
        "success": True,
        "token": token
    }

# função de fraude
def predict_fraud(transaction):
    score = 0

    if transaction["amount"] > 1000:
        score += 1

    if transaction["location"] != "BR":
        score += 1

    if random.random() > 0.7:
        score += 1

    return "FRAUDE" if score >= 2 else "OK"

# endpoint protegido
@app.post("/transactions/analyze", summary="Analisar transação para fraude")
def analyze_transaction(tx: Transaction, authorization: str = Header(...)):

    # validar token
    try:
        jwt.decode(authorization, SECRET, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

    status = predict_fraud(tx.dict())

    fake_db[tx.user_id] = status

    return {
        "success": True,
        "data": {
            "user_id": tx.user_id,
            "amount": tx.amount,
            "status": status
        },
        "message": "Transação analisada com sucesso"
    }

# consulta
@app.get("/transactions/{user_id}/status", summary="Consultar status da transação")
def get_status(user_id: int):
    status = fake_db.get(user_id, "Sem dados")

    return {
        "success": True,
        "data": {
            "user_id": user_id,
            "status": status
        }
    }
