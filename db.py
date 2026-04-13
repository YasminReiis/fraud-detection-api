fake_db = {}

def save_transaction(user_id, amount, status):
    fake_db[user_id] = status

def get_status(user_id):
    return fake_db.get(user_id, "Sem dados")
