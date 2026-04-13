import random

def predict_fraud(transaction):
    score = 0

    if transaction["amount"] > 1000:
        score += 1

    if transaction["location"] != "BR":
        score += 1

    if random.random() > 0.7:
        score += 1

    return 1 if score >= 2 else 0
