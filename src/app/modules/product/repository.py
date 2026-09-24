from sqlalchemy import String, cast, or_
from sqlalchemy.orm import Session

from app.models.product import Product


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products(
    db: Session,
    category: str | None = None,
    restaurant_id: int | None = None,
    is_available: bool | None = None,
    name_query: str | None = None,
):
    query = db.query(Product)

    if category is not None:
        query = query.filter(Product.category == category)
    if restaurant_id is not None:
        query = query.filter(Product.restaurant_id == restaurant_id)
    if is_available is not None:
        query = query.filter(Product.is_available == is_available)
    if name_query:
        search_pattern = f"%{name_query}%"
        query = query.filter(
            or_(
                cast(Product.id, String).ilike(search_pattern),
                Product.name.ilike(search_pattern),
                Product.image.ilike(search_pattern),
                Product.description.ilike(search_pattern),
                Product.category.ilike(search_pattern),
                cast(Product.price, String).ilike(search_pattern),
                cast(Product.is_available, String).ilike(search_pattern),
                cast(Product.restaurant_id, String).ilike(search_pattern),
                cast(Product.ingredients, String).ilike(search_pattern),
            )
        )

    return query.all()