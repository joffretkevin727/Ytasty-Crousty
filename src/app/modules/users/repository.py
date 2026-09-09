from pydantic import BaseModel, Field

class UsersRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    role: str = Field(..., pattern="^(admin|staff|direction)$")
    restaurant_id: int

class UsersResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    role: str = Field(..., pattern="^(admin|staff|direction)$")
    restaurant_id: int
