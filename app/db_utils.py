from sqlalchemy.orm import Session
from .models import User, Order


def create_user(db: Session, username: str, email: str, age: int) -> User:
    user = User(username=username, email=email, age=age)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_order(db: Session, user_id: int, product_name: str, quantity: int) -> Order:
    order = Order(user_id=user_id, product_name=product_name, quantity=quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()
