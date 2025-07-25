from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .db import get_db, engine, Base
from .pydantic_models import UserCreate, UserResponse, OrderCreate, OrderResponse
from . import db_utils, models
from .logger import log

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    log.info(f"Creating user {user.username}")
    if db.query(models.User).filter(
            (models.User.username == user.username) | (models.User.email == user.email)
    ).first():
        log.warning(f"Duplicate user {user.username}")
        raise HTTPException(status_code=400, detail="User already exists")
    return db_utils.create_user(db, user.username, user.email, user.age)


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db_utils.get_user(db, user_id)
    if not user:
        log.error(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    if not db_utils.get_user(db, order.user_id):
        log.error(f"User {order.user_id} not found for order")
        raise HTTPException(status_code=404, detail="User not found")
    return db_utils.create_order(db, order.user_id, order.product_name, order.quantity)


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db_utils.get_order(db, order_id)
    if not order:
        log.error(f"Order {order_id} not found")
        raise HTTPException(status_code=404, detail="Order not found")
    return order
