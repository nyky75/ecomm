import allure
from tests.utils.steps import step_create_user, step_create_order, step_get_order
from tests.utils.helpers import api_create_order


@allure.feature("Orders")
@allure.story("Создание заказа для пользователя")
@allure.title("Создание заказа для существующего пользователя")
@allure.description("""
Сценарий:
1. Создать нового пользователя (уникальные данные).
2. Создать заказ для него с товаром и количеством.
3. Получить заказ через API по ID.
4. Проверить, что данные совпадают с исходными.
""")
def test_create_order_for_user(client, get_user_data, get_order_data):
    # Шаг 1. Создаём пользователя с уникальными данными.
    user_data = get_user_data()
    user_id = step_create_user(client, **user_data)

    # Шаг 2. Генерируем данные заказа и создаём заказ.
    order_data = get_order_data()
    order_id = step_create_order(client, user_id, **order_data)

    # Шаг 3. Получаем заказ через API.
    order = step_get_order(client, order_id)

    # Шаг 4. Проверяем данные.
    assert order["product_name"] == order_data["product_name"], "Название товара не совпадает"
    assert order["quantity"] == order_data["quantity"], "Количество не совпадает"


@allure.feature("Orders")
@allure.story("Валидация при создании заказа")
@allure.title("Создание заказа с несуществующим пользователем должно возвращать 404")
@allure.description("""
Сценарий:
1. Попробовать создать заказ с user_id, которого нет в базе.
2. Проверить, что API возвращает 404 и сообщение "User not found".
""")
def test_order_for_invalid_user(client, get_order_data):
    # Шаг 1. Генерируем данные заказа (товар и количество).
    order_data = get_order_data()

    # Шаг 2. Пробуем создать заказ с несуществующим user_id.
    with allure.step("Создаём заказ с user_id=9999 (не существует)"):
        res = api_create_order(client, 9999, **order_data)

        # Шаг 3. Проверяем корректность ответа.
        assert res.status_code == 404, "Ожидался статус 404"
        assert res.json()["detail"] == "User not found", "Сообщение об ошибке некорректное"
