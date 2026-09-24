from sqlalchemy.orm import Session

from app.modules.product import repository


def get_product_by_id(db: Session, product_id: int):
    return repository.get_product_by_id(db, product_id)


def get_restaurant_ids(db: Session):
    return repository.get_restaurant_ids(db)


def create_products(db: Session, product_data: dict, restaurant_ids: list[int]):
    return repository.create_products(db, product_data, restaurant_ids)


def update_product(db: Session, product, product_data: dict):
    return repository.update_product(db, product, product_data)


def delete_product(db: Session, product):
    return repository.delete_product(db, product)


def get_all_products( db: Session, category: str | None = None, restaurant_id: int | None = None, is_available: bool | None = None, name_query: str | None = None):
    return repository.get_all_products( db, category=category, restaurant_id=restaurant_id, is_available=is_available, name_query=name_query)