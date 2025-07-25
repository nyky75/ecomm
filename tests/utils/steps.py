import allure
from app.logger import log
from tests.utils.helpers import api_create_user, api_get_user, api_create_order, api_get_order
from app.db_utils import User, Order


@allure.step("Создаем пользователя: {username}")
def step_create_user(client, username: str, email: str, age: int):
    log.info(f"Создаем пользователя username={username}, email={email}, age={age}")
    res = api_create_user(client, username, email, age)
    log.debug(f"Ответ API: {res.status_code} | {res.text}")
    assert res.status_code == 200, f"Ошибка создания пользователя: {res.text}"
    user_id = res.json()["id"]
    log.success(f"Пользователь создан с ID={user_id}")
    return user_id


@allure.step("Получаем пользователя с ID={user_id}")
def step_get_user(client, user_id):
    log.info(f"Запрос на получение пользователя ID={user_id}")
    res = api_get_user(client, user_id)
    log.debug(f"Ответ API: {res.status_code} | {res.text}")
    assert res.status_code == 200, f"Ошибка получения пользователя: {res.text}"
    data = res.json()
    log.success(f"Данные пользователя: {data}")
    return data


@allure.step("Создаем заказ для user_id={user_id}")
def step_create_order(client, user_id, product_name: str, quantity: int):
    log.info(f"Создаем заказ: user_id={user_id}, продукт={product_name}, количество={quantity}")
    res = api_create_order(client, user_id, product_name, quantity)
    log.debug(f"Ответ API: {res.status_code} | {res.text}")
    assert res.status_code == 200, f"Ошибка создания заказа: {res.text}"
    order_id = res.json()["id"]
    log.success(f"Заказ создан с ID={order_id}")
    return order_id


@allure.step("Получаем заказ с ID={order_id}")
def step_get_order(client, order_id):
    log.info(f"Запрос на получение заказа ID={order_id}")
    res = api_get_order(client, order_id)
    log.debug(f"Ответ API: {res.status_code} | {res.text}")
    assert res.status_code == 200, f"Ошибка получения заказа: {res.text}"
    data = res.json()
    log.success(f"Данные заказа: {data}")
    return data


@allure.step("Проверяем данные в БД для user_id={user_id}")
def step_check_db_user_and_orders(db_session, user_id: int, user_data: dict, api_order_ids: list[int], orders_count: int):
    """Проверяем, что пользователь и заказы реально существуют в БД и совпадают с API."""
    log.info(f"Проверяем данные в БД для пользователя ID={user_id}")
    db_user = db_session.query(User).filter_by(id=user_id).first()
    assert db_user is not None, "Пользователь не найден в БД"
    assert db_user.username == user_data["username"]

    db_orders = db_session.query(Order).filter_by(user_id=user_id).all()
    assert len(db_orders) == orders_count, f"В БД должно быть {orders_count} заказов"

    db_order_ids = [o.id for o in db_orders]
    assert sorted(db_order_ids) == sorted(api_order_ids), "ID заказов в БД и API не совпадают"
    log.success(f"Проверка данных в БД пройдена: пользователь и {orders_count} заказ(ов) совпадают с API")