from backend.repositories import cart_repo

def add(db, uid, data): 
    cart_repo.add(db, uid, data.product_id, data.quantity, data.size)

def items(db, uid): return cart_repo.items(db, uid)
def remove(db, iid): cart_repo.remove(db, iid)