from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(
        min_length=8,
        max_length=12,
        pattern=r"^[a-zA-Z0-9]+$"
    )

    password: str = Field(
        min_length=12,
        max_length=64
    )


class LoginResponse(BaseModel):
    access_token: str
    token_type: str