from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, ConfigDict


Username = Annotated[str, Field(min_length=3, pattern=r"^[A-Za-z0-9]+$")]
PositiveAge = Annotated[int, Field(gt=0, lt=100)]
PositiveQuantity = Annotated[int, Field(gt=0)]


class UserCreate(BaseModel):
    username: Username
    email: EmailStr
    age: PositiveAge


class UserResponse(UserCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    user_id: int
    product_name: str
    quantity: PositiveQuantity


class OrderResponse(OrderCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
