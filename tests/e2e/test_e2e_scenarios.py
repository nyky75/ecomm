import allure
import pytest
from tests.utils.steps import (
    step_create_user,
    step_get_user,
    step_create_order,
    step_get_order,
    step_check_db_user_and_orders,
)


@pytest.mark.parametrize("orders_count", [1, 3, 5])
@allure.feature("E2E")
@allure.story("Создание пользователя с заказами")
@allure.title("E2E: создание пользователя с {orders_count} заказ(ами) и проверка через БД")
@allure.description("""
Сценарий:
1. Создать нового пользователя (уникальные данные).
2. Создать N заказов (N задаётся параметризацией).
3. Проверить, что пользователь и все заказы корректно возвращаются через API.
4. Проверить данные напрямую из БД (пользователь и заказы совпадают с API).
""")
def test_e2e_user_with_orders(client, db_session, get_user_data, get_order_data, orders_count):
    # Шаг 1. Создаём пользователя с уникальными данными.
    user_data = get_user_data()
    user_id = step_create_user(client, **user_data)

    # Шаг 2. Создаём N заказов для этого пользователя (каждый заказ уникальный).
    created_orders = []
    for _ in range(orders_count):
        order_data = get_order_data()
        order_id = step_create_order(client, user_id, **order_data)
        created_orders.append({"id": order_id, **order_data})

    # Шаг 3. Проверяем пользователя через API (существует и корректен).
    api_user = step_get_user(client, user_id)
    assert api_user["username"] == user_data["username"], "Имя пользователя не совпадает"
    assert api_user["email"] == user_data["email"], "Email пользователя не совпадает"

    # Шаг 4. Проверяем все созданные заказы через API.
    api_order_ids = []
    for order in created_orders:
        order_from_api = step_get_order(client, order["id"])
        assert order_from_api["product_name"] == order["product_name"], "Название товара не совпадает"
        assert order_from_api["quantity"] == order["quantity"], "Количество не совпадает"
        api_order_ids.append(order_from_api["id"])

    # Шаг 5. Проверяем, что пользователь и все заказы реально есть в БД и совпадают с API.
    step_check_db_user_and_orders(db_session, user_id, user_data, api_order_ids, orders_count)
