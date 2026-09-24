from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.modules.orders.schema import OrderCreate, OrderResponse, OrderStatusUpdate, OrderStatus
from app.modules.orders.service import (
    create_order_service, get_order_service, get_restaurant_orders_service,
    update_order_status_service, cancel_order_service
)
from app.common.dependencies import get_db, get_current_user
from app.models.user import User

order_router = APIRouter(tags=["orders"])

@order_router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order_service(db, order)

@order_router.get("/orders/{order_number}", response_model=OrderResponse)
def get_order(order_number: str, db: Session = Depends(get_db)):
    return get_order_service(db, order_number)

@order_router.get("/restaurants/{restaurant_id}/orders", response_model=List[OrderResponse])
def get_restaurant_orders(
    restaurant_id: int, 
    status: Optional[OrderStatus] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_restaurant_orders_service(db, restaurant_id, status, current_user)

@order_router.patch("/orders/{order_number}/status", response_model=OrderResponse)
def update_order_status(
    order_number: str, 
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_order_status_service(db, order_number, status_update, current_user)

@order_router.post("/orders/{order_number}/cancel", response_model=OrderResponse)
def cancel_order(
    order_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cancel_order_service(db, order_number, current_user)
