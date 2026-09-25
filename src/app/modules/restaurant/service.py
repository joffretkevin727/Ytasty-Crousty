from app.modules.restaurant import repository
from sqlalchemy.orm import Session
from app.modules.restaurant.schemas import RestaurantUpdate



def get_all_restaurants(db: Session):
    return repository.get_all_restaurants(db)

def get_restaurants_by_id(db: Session, restaurant_id: int):
    return repository.get_restaurants_by_id(db, restaurant_id)


def modify_restaurant(db: Session, restaurant_id: int, restaurant_data: RestaurantUpdate):
    update_dict = restaurant_data.model_dump(exclude_unset=True)
    return repository.modify_restaurant(db, restaurant_id, update_dict)

def modify_restaurant_status(db: Session, restaurant_id: int, status: bool):
    return repository.modify_restaurant_status(db, restaurant_id, status)