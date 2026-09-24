"""Schema d'entrée et de sortie du module restaurant."""

from pydantic import BaseModel


class Product(BaseModel):
    id : int
    name : str
    image : str
    description : str
    category : str
    price : float
    is_available : bool
    restaurant_id : int
    ingredients : list[str]

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    name: str
    image: str
    description: str
    category: str
    price: float
    is_available: bool = True
    ingredients: list[str] = []