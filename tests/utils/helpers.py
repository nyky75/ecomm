from fastapi.testclient import TestClient


def api_create_user(client: TestClient, username: str, email: str, age: int):
    return client.post("/users", json={"username": username, "email": email, "age": age})


def api_get_user(client: TestClient, user_id: int):
    return client.get(f"/users/{user_id}")


def api_create_order(client: TestClient, user_id: int, product_name: str, quantity: int = 1):
    return client.post("/orders", json={"user_id": user_id, "product_name": product_name, "quantity": quantity})


def api_get_order(client: TestClient, order_id: int):
    return client.get(f"/orders/{order_id}")
