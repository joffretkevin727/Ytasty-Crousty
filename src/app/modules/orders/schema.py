from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    validated = "validated"
    preparing = "preparing"
    ready = "ready"
    collected = "collected"
    cancelled = "cancelled"

class PickupMode(str, Enum):
    onsite = "onsite"
    takeaway = "takeaway"

class Customer(BaseModel):
    name: str
    email: str

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    restaurant_id: int
    items: List[OrderItemCreate]
    pickup_mode: PickupMode
    customer: Customer

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    model_config = {"from_attributes": True}

class OrderResponse(BaseModel):
    order_number: str
    restaurant_id: int
    created_at: datetime
    items: List[OrderItemResponse]
    total_price: float
    status: OrderStatus
    pickup_mode: PickupMode
    customer: Customer
    model_config = {"from_attributes": True}

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
