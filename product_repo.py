from sqlalchemy.orm import Session
from backend.models.product import Product
from backend.schemas.product import ProductIn, CatalogFilter

def create(db: Session, data: ProductIn):
    p = Product(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def get(db: Session, pid):
    return db.query(Product).get(pid)

def search(db: Session, f: CatalogFilter):
    q = db.query(Product)
    
    # 1. ПОИСК ПО СЛОВУ
    if f.query:
        # Убираем лишние пробелы, которые Flet мог добавить
        clean_query = f.query.strip()
        q = q.filter(Product.name.ilike(f"%{clean_query}%"))
        
    # 2. ФИЛЬТР ПО ТИПУ (Одежда/Обувь)
    if f.type and str(f.type).strip() != "":
        q = q.filter(Product.type == f.type.strip())
        
    # 3. ФИЛЬТР ПО УРОВНЮ (Новичок/Профи)
    if f.category and str(f.category).strip() != "":
        q = q.filter(Product.category == f.category.strip())
        
    # 4. ФИЛЬТР ПО БРЕНДУ
    if f.brand and str(f.brand).strip() != "":
        q = q.filter(Product.brand == f.brand.strip())

    # 5. ОСТАЛЬНЫЕ ФИЛЬТРЫ
    if f.min_price is not None:
        q = q.filter(Product.price >= f.min_price)
    if f.max_price is not None:
        q = q.filter(Product.price <= f.max_price)
    if f.size:
        q = q.filter(Product.size.ilike(f"%{f.size}%"))
    if f.color:
        q = q.filter(Product.color == f.color)
    if f.availability is not None:
        q = q.filter(Product.availability == f.availability)

    # 6. СОРТИРОВКА
    if f.sort_by == "new":
        q = q.order_by(Product.id.desc())
    else:
        q = q.order_by(Product.name.asc())

    # Отладочный вывод (посмотри в консоли uvicorn)
    print(f"--- ЗАПРОС В БД ---")
    print(f"Ищем: Тип={f.type}, Уровень={f.category}, Бренд={f.brand}")
    print(f"Найдено записей: {q.count()}")
    
    return q.offset(f.offset).limit(f.limit).all()

def update(db: Session, pid, data: ProductIn):
    p = get(db, pid)
    if not p:
        return None
    for k, v in data.model_dump().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

def delete(db: Session, pid):
    p = get(db, pid)
    if not p:
        return False
    db.delete(p)
    db.commit()
    return True