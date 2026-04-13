from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_fraud
from db import save_transaction, get_status

app = FastAPI()

class Transaction(BaseModel):
    user_id: int
    amount: float
    location: str

@app.post("/transaction")
def process_transaction(tx: Transaction):
    result = predict_fraud(tx.dict())
    status = "FRAUDE" if result == 1 else "OK"

    save_transaction(tx.user_id, tx.amount, status)

    return {"status": status}

@app.get("/status/{user_id}")
def check_status(user_id: int):
    return {"status": get_status(user_id)}
