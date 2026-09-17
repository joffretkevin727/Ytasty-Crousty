from passlib.context import CryptContext

from app.modules.users import repository
from app.modules.users.schemas import UsersRequest


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def create_user(req: UsersRequest, db):
    existing_user = repository.get_user_by_username(
        db,
        req.username
    )

    if existing_user is not None:
        return None

    password_hash = pwd_context.hash(req.password)

    return repository.create_user(
        db=db,
        first_name=req.first_name,
        last_name=req.last_name,
        username=req.username,
        password_hash=password_hash,
        role=req.role,
        restaurant_id=req.restaurant_id
    )
