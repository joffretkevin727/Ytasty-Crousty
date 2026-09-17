from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_username(db: Session, username: str):
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def create_user(
    db: Session,
    first_name: str,
    last_name: str,
    username: str,
    password_hash: str,
    role: str,
    restaurant_id: int | None
):
    user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password_hash=password_hash,
        role=role,
        restaurant_id=restaurant_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
