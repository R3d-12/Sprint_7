import requests
import allure
from utils.helpers import register_new_courier_and_return_login_password, BASE_URL, generate_random_string

@allure.suite("API Курьеров")
@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    def test_login_success(self):
        courier = register_new_courier_and_return_login_password()
        payload = {"login": courier["login"], "password": courier["password"]}
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Попытка авторизации с неправильными данными")
    def test_login_wrong_credentials(self):
        payload = {"login": "wrong", "password": "wrong"}
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        assert response.status_code == 404

    @allure.title("Попытка авторизации без login")
    def test_login_missing_login(self):
        payload = {"password": generate_random_string()}
        response = requests.post(f"{BASE_URL}/courier/login", json=payload, timeout=5)
        assert response.status_code == 400, f"Ожидался 400, получили {response.status_code}"

    @allure.title("Попытка авторизации без password")
    def test_login_missing_password(self):
        payload = {"login": generate_random_string()}
        response = requests.post(f"{BASE_URL}/courier/login", json=payload, timeout=5)
        assert response.status_code == 400, f"Ожидался 400, получили {response.status_code}"