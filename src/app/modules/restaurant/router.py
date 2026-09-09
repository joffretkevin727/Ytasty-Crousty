from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

from app.modules.restaurant import service
from app.modules.restaurant.schemas import RestaurantResponse

restaurant_router = APIRouter(tags=["Restaurant"])

@restaurant_router.get("/restaurants", response_model=RestaurantResponse, status_code=201)
def get_restaurant():
    return service.get_all_restaurants()

@restaurant_router.get("/restaurants/{restaurant_id}", response_model=Restaurant, status_code=201)
def get_restaurant_by_id(restaurant_id: int):
    return service.get_restaurants_by_id(restaurant_id)

""" route réservée aux admins"""

@restaurant_router.put("/restaurants/{restaurant_id}", status_code=201)
def modify_restaurant(restaurant_id: int):
    return service.modify_restaurant()

@restaurant_router.put("/restaurants/{restaurant_id}/status", status_code=201)
def modify_restaurant_status(restaurant_id: int):
    return service.modify_restaurant_status()