from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant


def get_all_restaurants(db: Session):
    return db.query(Restaurant).all()

def get_restaurants_by_id(db: Session, restaurant_id: int):
    return (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

""" route réservée aux admins"""

def modify_restaurant(db: Session, restaurant_id: int, restaurant_data: dict):
    restaurant = (
      db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
  )
    if restaurant:
        for key, value in restaurant_data.items():
            setattr(restaurant, key, value)
        db.commit()
        db.refresh(restaurant)
    return restaurant

def modify_restaurant_status(db: Session, restaurant_id: int, status: bool):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if restaurant:
        restaurant.is_open = status
        db.commit()
        db.refresh(restaurant)
    return restaurant


