from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "change-this-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {
    "admin123": {
        "username": "admin123",
        "password_hash": pwd_context.hash("Admin@123456"),
        "role": "admin",
    }
}


def auth(username: str, password: str):
    user = users.get(username)

    if user is None:
        return None

    if not pwd_context.verify(password, user["password_hash"]):
        return None

    token = jwt.encode(
        {
            "sub": user["username"],
            "role": user["role"],
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }