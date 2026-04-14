from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import random
import jwt

SECRET = "super_secret_key"

app = FastAPI(
    title="🚨 Real-Time Fraud Detection API",
    description="Production-ready API with authentication",
    version="3.0.0"
)

fake_db = {}

class Transaction(BaseModel):
    user_id: int
    amount: float
    location: str

def build_response(success, data=None, message="", error=None):
    return {
        "success": success,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
        "message": message,
        "error": error
    }

def predict_fraud(transaction):
    score = 0

    if transaction["amount"] > 1000:
        score += 1
    if transaction["location"] != "BR":
        score += 1
    if random.random() > 0.7:
        score += 1

    return "FRAUDE" if score >= 2 else "OK"

def verify_token(token):
    try:
        jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def home():
    return build_response(True, {"service": "fraud-api"}, "Running")

@app.get("/health")
def health():
    return build_response(True, {"status": "ok"}, "Healthy")

# 🔐 LOGIN
@app.post("/v1/auth/login")
def login():
    token = jwt.encode({"user_id": 1}, SECRET, algorithm="HS256")
    return build_response(True, {"token": token}, "Token generated")

# 🔒 PROTEGIDO
@app.post("/v1/transactions/analyze")
def analyze_transaction(tx: Transaction, authorization: str = Header(...)):

    verify_token(authorization)

    status = predict_fraud(tx.dict())
    fake_db[tx.user_id] = status

    return build_response(True, {
        "user_id": tx.user_id,
        "amount": tx.amount,
        "status": status
    }, "Transaction processed")

@app.get("/v1/transactions/{user_id}/status")
def get_status(user_id: int, authorization: str = Header(...)):

    verify_token(authorization)

    status = fake_db.get(user_id, "Sem dados")

    return build_response(True, {
        "user_id": user_id,
        "status": status
    }, "OK")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=build_response(False, None, "Internal error", str(exc)),
    )
