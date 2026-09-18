from app.modules.product import repository
from sqlalchemy.orm import Session




def get_all_products(
    db: Session,
    category: str | None = None,
    restaurant_id: int | None = None,
    is_available: bool | None = None,
    name_query: str | None = None,
):
    return repository.get_all_products(
        db,
        category=category,
        restaurant_id=restaurant_id,
        is_available=is_available,
        name_query=name_query,
    )