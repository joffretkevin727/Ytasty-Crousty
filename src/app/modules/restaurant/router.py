from fastapi import APIRouter, HTTPException, Depends, status

from app.common.dependencies import get_current_user, get_db
from app.models.user import User
from app.modules.restaurant import service
from app.modules.restaurant.schemas import Restaurant, RestaurantStatusUpdate, RestaurantUpdate

restaurant_router = APIRouter(tags=["Restaurant"])

@restaurant_router.get("/restaurants", response_model=list[Restaurant])
def get_restaurant(db=Depends(get_db)):
    result = service.get_all_restaurants(db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No restaurants found"
        )
    return result

@restaurant_router.get("/restaurants/{restaurant_id}", response_model=Restaurant)
def get_restaurant_by_id(restaurant_id: int, db=Depends(get_db)):
    result = service.get_restaurants_by_id(db, restaurant_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    return result

""" route réservée aux admins"""

@restaurant_router.put("/restaurants/{restaurant_id}", response_model=Restaurant)
def modify_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can modify restaurants",
        )

    result = service.modify_restaurant(db, restaurant_id, restaurant_data)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    return result

@restaurant_router.put("/restaurants/{restaurant_id}/availability", response_model=RestaurantStatusUpdate)
def modify_restaurant_status(
    restaurant_id: int,
    status_data: RestaurantStatusUpdate,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can modify restaurant availability",
        )

    result = service.modify_restaurant_status(db, restaurant_id, status_data.is_open)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    return result