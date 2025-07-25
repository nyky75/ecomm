import pytest
import allure
from pydantic import ValidationError
from app.pydantic_models import UserCreate, OrderCreate


@allure.feature("Validation")
@allure.story("Проверка валидации данных пользователя")
@allure.title("Негативные проверки UserCreate (валидаторы)")
@allure.description("""
Сценарий:
1. Пробуем создать UserCreate с некорректными значениями полей.
2. Проверяем, что Pydantic выбрасывает ValidationError.
3. Покрываем кейсы: короткий username, запрещённые символы, невалидный email, 
   граничные значения возраста (0 и 100).
""")
@pytest.mark.parametrize("username, email, age", [
    ("ab", "valid@mail.com", 25),          # слишком короткий username (<3)
    ("abc$", "valid@mail.com", 25),        # недопустимые символы
    ("validUser", "not-an-email", 25),     # невалидный email
    ("validUser", "valid@mail.com", 0),    # возраст ниже границы
    ("validUser", "valid@mail.com", 100),  # возраст выше границы
])
def test_invalid_user_data(username, email, age):
    with allure.step(f"Пробуем создать UserCreate с {username=}, {email=}, {age=}"):
        with pytest.raises(ValidationError):
            UserCreate(username=username, email=email, age=age)


@allure.feature("Validation")
@allure.story("Проверка валидации данных заказа")
@allure.title("Негативные проверки OrderCreate (валидаторы)")
@allure.description("""
Сценарий:
1. Пробуем создать OrderCreate с некорректными значениями полей.
2. Проверяем, что Pydantic выбрасывает ValidationError.
3. Покрываем кейсы: количество = 0, отрицательное количество, пустое название товара.
""")
@pytest.mark.parametrize("user_id, product_name, quantity", [
    (1, "Laptop", 0),    # количество = 0
    (1, "Laptop", -1),   # отрицательное количество
    (1, "", 1),          # пустое название товара
])
def test_invalid_order_data(user_id, product_name, quantity):
    with allure.step(f"Пробуем создать OrderCreate с {user_id=}, {product_name=}, {quantity=}"):
        with pytest.raises(ValidationError):
            OrderCreate(user_id=user_id, product_name=product_name, quantity=quantity)
