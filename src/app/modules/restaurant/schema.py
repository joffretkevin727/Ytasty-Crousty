"""Schema d'entrée et de sortie du module restaurant."""

from pydantic import BaseModel


class Restaurant(BaseModel):
    id: int
    name: str
    city: str
    adress: str
    is_open: bool
    opening_hours: str
    contact: str
    
class RestaurantResponse(BaseModel):
    list: list[Restaurant]