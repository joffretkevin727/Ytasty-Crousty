from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.restaurant import Restaurant

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_order_db(db: Session, order: Order):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_order_by_number(db: Session, order_number: str):
    return db.query(Order).filter(Order.order_number == order_number).first()

def get_orders_by_restaurant(db: Session, restaurant_id: int, status: str = None):
    query = db.query(Order).filter(Order.restaurant_id == restaurant_id)
    if status:
        query = query.filter(Order.status == status)
    return query.all()

def update_order_db(db: Session, order: Order):
    db.commit()
    db.refresh(order)
    return order
