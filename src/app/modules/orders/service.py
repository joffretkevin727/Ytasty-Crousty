from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid

from app.modules.orders.schema import OrderCreate, OrderStatus, OrderStatusUpdate
from app.modules.orders.repository import (
    get_product_by_id, create_order_db, get_order_by_number,
    get_orders_by_restaurant, update_order_db
)
from app.modules.restaurant.repository import get_restaurants_by_id
from app.models.order import Order, OrderItem
from app.models.user import User

def create_order_service(db: Session, order_req: OrderCreate):
    restaurant = get_restaurants_by_id(db, order_req.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=400, detail="Restaurant does not exist")
    if not restaurant.is_open:
        raise HTTPException(status_code=400, detail="Restaurant is closed")

    total_price = 0.0
    order_items = []

    for item_req in order_req.items:
        if item_req.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

        product = get_product_by_id(db, item_req.product_id)
        if not product:
            raise HTTPException(status_code=400, detail=f"Product {item_req.product_id} does not exist")
        
        if product.restaurant_id != order_req.restaurant_id:
            raise HTTPException(status_code=400, detail=f"Product {item_req.product_id} belongs to another restaurant")
        
        if not product.is_available:
            raise HTTPException(status_code=400, detail=f"Product {item_req.product_id} is unavailable")

        unit_price = float(product.price)
        total_price += unit_price * item_req.quantity
        
        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item_req.quantity,
                unit_price=unit_price
            )
        )

    order_number = uuid.uuid4().hex[:16].upper()

    order = Order(
        order_number=order_number,
        restaurant_id=order_req.restaurant_id,
        total_price=total_price,
        status=OrderStatus.pending.value,
        pickup_mode=order_req.pickup_mode.value,
        customer=order_req.customer.model_dump(),
        items=order_items
    )

    return create_order_db(db, order)

def get_order_service(db: Session, order_number: str):
    order = get_order_by_number(db, order_number)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def check_permissions(user: User, restaurant_id: int):
    if user.role == "staff" and user.restaurant_id != restaurant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this restaurant")

def get_restaurant_orders_service(db: Session, restaurant_id: int, status_filter: OrderStatus, current_user: User):
    restaurant = get_restaurants_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    check_permissions(current_user, restaurant_id)
    
    status_str = status_filter.value if status_filter else None
    return get_orders_by_restaurant(db, restaurant_id, status_str)

def update_order_status_service(db: Session, order_number: str, status_update: OrderStatusUpdate, current_user: User):
    order = get_order_by_number(db, order_number)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    check_permissions(current_user, order.restaurant_id)

    order.status = status_update.status.value
    return update_order_db(db, order)

def cancel_order_service(db: Session, order_number: str, current_user: User):
    order = get_order_by_number(db, order_number)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    check_permissions(current_user, order.restaurant_id)

    order.status = OrderStatus.cancelled.value
    return update_order_db(db, order)
