from jose import jwt
from passlib.context import CryptContext

from app.modules.auth.repository import LoginResponse

SECRET_KEY = "7gu6u3_s)!(mor*zdv4-d2w_z855(=owtxdw8nu)jfylf4_$+#"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {
    "admin123": {
        "username": "admin123",
        "password_hash": pwd_context.hash("Admin@123456"),
        "role": "admin",
    }
}

def auth(req):
    user = users.get(req.username)

    if user is None:
        return None

    if not pwd_context.verify(req.password, user["password_hash"]):
        return None

    token = jwt.encode(
        {
            "sub": user["username"],
            "role": user["role"],
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return LoginResponse(access_token=token, token_type="bearer")
 