import requests
import allure
from utils.helpers import register_new_courier_and_return_login_password, BASE_URL, generate_random_string

@allure.suite("API Курьеров")
@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    def test_login_success(self):
        with allure.step("Создание нового курьера"):
            response, courier_data = register_new_courier_and_return_login_password()

        payload = {"login": courier_data["login"], "password": courier_data["password"]}

        with allure.step("Отправка запроса на авторизацию"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload, timeout=15)
            data = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"

        with allure.step("Проверка, что в ответе есть id"):
            assert "id" in data, f"В ответе нет id: {data}"

    @allure.title("Попытка авторизации с неправильными данными")
    def test_login_wrong_credentials(self):
        payload = {"login": "wrong", "password": "wrong"}

        with allure.step("Отправка запроса на авторизацию с неверными данными"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload, timeout=15)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}"

    @allure.title("Попытка авторизации без login")
    def test_login_missing_login(self):
        payload = {"password": generate_random_string()}

        with allure.step(f"Отправка запроса без login, payload={payload}"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload, timeout=15)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 400, f"Ожидался 400, получили {response.status_code}"

    @allure.title("Попытка авторизации без password")
    def test_login_missing_password(self):
        payload = {"login": generate_random_string()}

        with allure.step(f"Отправка запроса без password, payload={payload}"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload, timeout=15)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 400, f"Ожидался 400, получили {response.status_code}"