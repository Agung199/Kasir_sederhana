from fastapi import FastAPI, Depends, HTTPException
from database import engine, Base
from sqlalchemy.orm import Session

from database import get_db
from models import User, Item, StockMovement
from schemas import UserRegister, ItemCreate, ItemUpdate, StockRequest, UserLogin


app = FastAPI(title="Kasir Api")

Base.metadata.create_all(bind=engine)


@app.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user_data.username).first()

    if existing:
        raise HTTPException(status_code=400, detail="Username sudah digunakan")

    user = User(username=user_data.username, email=user_data.email)

    user.set_password(user_data.password)

    db.add(user)
    db.commit()

    return {"message": "Registrasi berhasil"}


@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")

    if not user.check_password(user_data.password):
        raise HTTPException(status_code=401, detail="Password Salah")

    return {
        "message": "Login Berhasil",
        "user": {"id": user.id, "username": user.username, "email": user.email},
    }


@app.post("/items")
def create_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    item = Item(name=item_data.name, stock=item_data.stock, price=item_data.price)

    db.add(item)
    db.commit()
    db.refresh(item)

    return {"id": item.id, "name": item.name, "stock": item.stock, "price": item.price}


@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()

    return [
        {"id": item.id, "name": item.name, "stock": item.stock, "price": item.price}
        for item in items
    ]


@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")

    return {"id": item.id, "name": item.name, "stock": item.stock, "price": item.price}


@app.put("/items/{item_id}")
def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")

    if item_data.name is not None:
        item.name = item_data.name

    if item_data.name is not None:
        item.stock = item_data.stock

    if item_data.price is not None:
        item.price = item_data.price

    db.commit()
    db.refresh(item)

    return {
        "message": "Item berhasil diupdate",
        "item": {
            "id": item.id,
            "name": item.name,
            "stock": item.stock,
            "price": item.price,
        },
    }


@app.delete("/items/{items_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    db.delete(item)
    db.commit()

    return {"message": "Item berhasil dihapus"}


# stock in
@app.post("/stock-in")
def stock_in(data: StockRequest, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == data.item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    item.stock += data.quantity

    movement = StockMovement(
        item_id=item.id, movement_type="IN", quantity=data.quantity, notes=data.notes
    )

    db.add(movement)
    db.commit()

    return {"message": "Stock berhasil ditambahkan", "current_stock": item.stock}


# stock out
@app.post("/stock-out")
def stock_out(data: StockRequest, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == data.item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")

    if item.stock < data.quantity:
        raise HTTPException(status_code=400, detail="Stock tidak mencukupi")

    item.stock -= data.quantity

    movement = StockMovement(
        item_id=item.id, movement_type="OUT", quantity=data.quantity, notes=data.notes
    )

    db.add(movement)
    db.commit()

    return {"message": "Stock berhasil dikurangi", "current_stock": item.stock}


# Riwayat Mutasi
@app.get("/movements")
def get_movements(db: Session = Depends(get_db)):
    movements = db.query(StockMovement).order_by(StockMovement.created_at.desc()).all()

    return [
        {
            "id": m.id,
            "item_id": m.item_id,
            "item_name": m.item.name,
            "type": m.movement_type,
            "quantity": m.quantity,
            "notes": m.notes,
            "created_at": m.created_at,
        }
        for m in movements
    ]
