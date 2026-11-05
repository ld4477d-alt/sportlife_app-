from backend.repositories import favorite_repo


def toggle(db, uid, pid):
    favs = favorite_repo.for_user(db, uid)
    if any(f.product_id == pid for f in favs):
        favorite_repo.remove(db, uid, pid)
        return False
    favorite_repo.add(db, uid, pid)
    return True


def list_favs(db, uid):
    return favorite_repo.for_user(db, uid)