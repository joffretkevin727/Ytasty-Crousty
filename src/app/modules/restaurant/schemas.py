
from pydantic import BaseModel


class Restaurant(BaseModel):
    id: int
    name: str
    city: str
    address: str
    is_open: bool
    opening_hours: str
    contact: str

    model_config = {"from_attributes": True}

class RestaurantResponse(BaseModel):
    list: list[Restaurant]

class RestaurantUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    address: str | None = None
    opening_hours: str | None = None
    contact: str | None = None

    model_config = {"from_attributes": True}


class RestaurantStatusUpdate(BaseModel):
    is_open: bool