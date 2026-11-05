from backend.repositories import product_repo


def list_products(db, f):
    return product_repo.search(db, f)


def get(db, pid):
    return product_repo.get(db, pid)


def create(db, data):
    return product_repo.create(db, data)


def update(db, pid, data):
    return product_repo.update(db, pid, data)


def delete(db, pid):
    return product_repo.delete(db, pid)