from flask import Flask, request, jsonify
from config import Config
from models import db, Item, User, StockMovement
from sqlalchemy import text
from fastapi import FastAPI


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# -------------------
# INIT DATABASE
# -------------------
with app.app_context():
    print("Creating tables...")
    db.create_all()
    print("Done")

# ------------------
# Register
# -------------------


@app.route("/register", methods=["POST"])
def register():

    data = request.json

    existing_user = User.query.filter_by(username=data["username"]).first()

    if existing_user:
        return jsonify({"message": "username sudah digunakan"}), 400

    user = User(username=data["username"], email=data["email"])

    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registrasi berhasil"}), 201


# -------------------
# Endpoint Login
# -------------------


@app.route("/login", methods=["POST"])
def login():

    data = request.json

    user = User.query.filter_by(username=data["username"]).first()

    if not user:
        return jsonify({"message": "User tidak ditemukan"}), 401
    if not user.check_password(data["password"]):
        return jsonify({"message": "password salah"}), 401

    return jsonify(
        {
            "message": "Login berhasil",
            "user": {"id": user.id, "username": user.username, "email": user.email},
        }
    ), 200


# print(app.url_map)


# -------------------
# CREATE ITEM
# -------------------
@app.route("/items", methods=["POST"])
def create_item():
    data = request.json

    item = Item(name=data["name"], stock=data["stock"], price=data["price"])

    db.session.add(item)
    db.session.commit()

    return jsonify(item.to_dict()), 201


# -------------------
# GET ALL ITEMS
# -------------------
@app.route("/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    return jsonify([i.to_dict() for i in items])


# -------------------
# GET ONE ITEM
# -------------------
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())


# -------------------
# UPDATE ITEM
# -------------------
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.json

    item.name = data.get("name", item.name)
    item.stock = data.get("stock", item.stock)
    item.price = data.get("price", item.price)

    db.session.commit()

    return jsonify(item.to_dict())


# -------------------
# DELETE ITEM
# -------------------
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Item deleted"})


with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))
        print("DATABASE CONNECTED")
    except Exception as e:
        print("DATABASE ERROR:", e)


# Tambah Stock Movement
@app.route("/stock-in", methods=["POST"])
def stock_in():

    data = request.get_json()

    item = Item.query.get_or_404(data["item_id"])

    qty = int(data["quantity"])

    if qty <= 0:
        return jsonify({"error": "Quantity harus lebih dari 0 "}), 400

    # Tambah Stock
    item.stock += qty

    # simpan history
    movement = StockMovement(
        item_id=item.id, movement_type="IN", quantity=qty, notes=data.get("notes", "")
    )

    db.session.add(movement)
    db.session.commit()

    return jsonify(
        {
            "message": "Stock berhasil ditambahkan",
            "item_id": item.id,
            "item_name": item.name,
            "current_stock": item.stock,
        }
    ), 201


# Endpoint Riwayat Mutasi
@app.route("/movements", methods=["GET"])
def get_movement():

    movements = StockMovement.query.order_by(StockMovement.created_at.desc()).all()

    result = []

    for m in movements:
        result.append(
            {
                "id": m.id,
                "item_id": m.item_id,
                "item_name": m.item.name,
                "type": m.movement_type,
                "quantity": m.quantity,
                "notes": m.notes,
                "created_at": m.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return jsonify(result)


# Endpoin stock out
@app.route("/stock-out", methods=["POST"])
def stock_out():
    data = request.get_json()

    item = Item.query.get_or_404(data["item_id"])

    qty = int(data["quantity"])

    if qty <= 0:
        return jsonify({"error": "Quantity harus lebih dari 0"}), 400

    # cek stock tersedia
    if item.stock < qty:
        return jsonify(
            {"error": "Stock tidak mencukupi", "cuurent_stock": item.stock}
        ), 400

    # kurangi stock
    item.stock -= qty

    # simpan history
    movement = StockMovement(
        item_id=item.id, movement_type="out", quantity=qty, notes=data.get("notes", "")
    )

    db.session.add(movement)
    db.session.commit()

    return jsonify(
        {
            "message": "Stock berhasil dikurangi",
            "item_id": item.id,
            "item_name": item.name,
            "current_stock": item.stock,
        }
    ), 200


# -------------------
# RUN APP
# -------------------
if __name__ == "__main__":
    app.run(debug=True)
