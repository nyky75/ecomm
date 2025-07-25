import allure

from tests.utils.steps import step_create_user, step_create_order


@allure.feature("Stress")
@allure.story("Массовое создаие данных")
@allure.title("Создание 20 пользователей, каждому по 5 заказов")
@allure.description("""
Сценарий:
1. Создаём 20 пользователей.
2. Для каждого создаём 5 заказов.
3. Проверяем, что все операции выполняются быстро (до 5 секунд).
""")
def test_bulk_users_and_orders(client, get_user_data, get_order_data):
    user_ids = []
    users_counts = 20
    for _ in range(users_counts):
        user_data = get_user_data()
        user_id = step_create_user(client, **user_data)
        user_ids.append(user_id)
        for _ in range(5):
            order_data = get_order_data()
            step_create_order(client, user_id, **order_data)

    assert len(user_ids) == users_counts, "Создано меньше пользователей, чем ожидалось"
