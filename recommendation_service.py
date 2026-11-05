from backend.repositories import view_history_repo, product_repo
from backend.models.product import Product
from backend.schemas.product import CatalogFilter


def log_view(db, uid, pid):
    view_history_repo.log(db, uid, pid)


def recommend(db, uid, limit=6):
    viewed = view_history_repo.last(db, uid)
    if not viewed:
        return product_repo.search(db, CatalogFilter(sort_by="new", limit=limit))

    pids = [v.product_id for v in viewed]
    prods = db.query(Product).filter(Product.id.in_(pids)).all()
    cats = {p.category_id for p in prods if p.category_id}

    if not cats:
        return product_repo.search(db, CatalogFilter(sort_by="new", limit=limit))

    return (db.query(Product)
            .filter(Product.category_id.in_(cats), ~Product.id.in_(pids))
            .limit(limit).all())