from fastapi import APIRouter, Depends, HTTPException, status

from app.common.dependencies import get_db
from app.modules.product import service
from app.modules.product.schemas import Product

product_router = APIRouter(tags=["Product"])

@product_router.get("/products", response_model=list[Product])
def get_products( category: str | None = None, restaurant_id: int | None = None, is_available: bool | None = None, q: str | None = None, db=Depends(get_db)):
    result = service.get_all_products(
        db,
        category=category,
        restaurant_id=restaurant_id,
        is_available=is_available,
        name_query=q,
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")
    return result


@product_router.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int, db=Depends(get_db)):
    result = service.get_product_by_id(db, product_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return result