import requests
import random
import string
import allure

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

@allure.step("Генерация случайной строки длиной {length}")
def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

@allure.step("Регистрация нового курьера")
def register_new_courier_and_return_login_password():
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()
    payload = {"login": login, "password": password, "firstName": first_name}
    with allure.step(f"Отправка POST /courier с логином {login}"):
        response = requests.post(f"{BASE_URL}/courier", json=payload)
    if response.status_code == 201:
        return {"login": login, "password": password, "firstName": first_name}
    return {}

@allure.step("Авторизация курьера с логином {login}")
def login_courier(login, password):
    payload = {"login": login, "password": password}
    with allure.step(f"Отправка POST /courier/login"):
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
    if response.status_code == 200:
        return response.json().get("id")
    return None

@allure.step("Создание заказа с данными {order_data}")
def create_order(order_data):
    with allure.step("Отправка POST /orders"):
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
    if response.status_code == 201:
        return response.json().get("track")
    return None