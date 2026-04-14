from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI(
    title="🚨 Real-Time Fraud Detection API",
    description="""
Production-ready API for fraud detection.

Features:
- Transaction analysis
- Fraud detection logic
- Standardized responses
- Global error handling
- Health check endpoint
- API versioning (/v1)

Use case:
Simulates how financial systems detect suspicious transactions in real-time.
""",
    version="2.0.0"
)

# banco simples (simulação)
fake_db = {}

# ==============================
# MODELS
# ==============================

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

# ==============================
# UTIL
# ==============================

def build_response(success: bool, data=None, message="", error=None):
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

# ==============================
# ROUTES
# ==============================

@app.get("/", summary="Home")
def home():
    return build_response(
        True,
        {
            "service": "fraud-detection-api",
            "version": "2.0.0",
            "docs": "/docs"
        },
        "API is running"
    )

@app.get("/health", summary="Health Check")
def health():
    return build_response(True, {"status": "ok"}, "Service healthy")

@app.post("/v1/transactions/analyze", summary="Analyze transaction for fraud")
def analyze_transaction(tx: Transaction):
    status = predict_fraud(tx.dict())

    fake_db[tx.user_id] = status

    return build_response(
        True,
        {
            "user_id": tx.user_id,
            "amount": tx.amount,
            "status": status
        },
        "Transaction processed successfully"
    )

@app.get("/v1/transactions/{user_id}/status", summary="Get transaction status")
def get_status(user_id: int):
    status = fake_db.get(user_id, "Sem dados")

    return build_response(
        True,
        {
            "user_id": user_id,
            "status": status
        },
        "Status retrieved successfully"
    )

# ==============================
# GLOBAL ERROR HANDLER
# ==============================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=build_response(
            False,
            None,
            "Internal server error",
            str(exc)
        ),
    )
