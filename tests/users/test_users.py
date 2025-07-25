import allure
from tests.utils.steps import step_create_user, step_get_user
from tests.utils.helpers import api_create_user


@allure.feature("Users")
@allure.story("Создание и получение пользователя")
@allure.title("Создание и получение уникального пользователя")
@allure.description("""
Сценарий:
1. Создать нового пользователя с уникальными данными.
2. Получить пользователя через API по его ID.
3. Проверить, что данные (username и email) совпадают с исходными.
""")
def test_create_and_get_user(client, get_user_data):
    # Шаг 1. Генерируем уникальные данные и создаём пользователя.
    user_data = get_user_data()
    user_id = step_create_user(client, **user_data)

    # Шаг 2. Получаем пользователя через API.
    user = step_get_user(client, user_id)

    # Шаг 3. Проверяем, что данные совпадают.
    assert user["username"] == user_data["username"], "Имя пользователя не совпадает"
    assert user["email"] == user_data["email"], "Email не совпаает"


@allure.feature("Users")
@allure.story("Валидация при создании")
@allure.title("Создание дубликата пользователя вызывает ошибку")
@allure.description("""
Сценарий:
1. Создать нового пользователя с уникальными данными.
2. Попробовать создать такого же пользователя (дубликат).
3. Проверить, что API возвращает ошибку 400 и сообщение "User already exists".
""")
def test_duplicate_user_rejected(client, get_user_data):
    # Шаг 1. Генерируем уникальные данные и создаём пользователя.
    user_data = get_user_data()
    step_create_user(client, **user_data)

    # Шаг 2. Пробуем создать дубликат.
    with allure.step("Пробуем создать дубликат пользователя"):
        res = api_create_user(client, **user_data)

        # Шаг 3. Проверяем, что вернулась ошибка.
        assert res.status_code == 400, "Ожидался статус 400"
        assert res.json()["detail"] == "User already exists", "Неверное сообщение об ошибке"
