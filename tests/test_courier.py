import requests
import allure
from utils.helpers import register_new_courier_and_return_login_password, BASE_URL, generate_random_string

@allure.suite("API Курьеров")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        courier = register_new_courier_and_return_login_password()
        assert courier != {}, "Курьер не был создан"

    @allure.title("Попытка создания курьера без обязательного поля")
    def test_create_courier_missing_login(self):
        payload = {"password": generate_random_string()}
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 400

    @allure.title("Попытка создания курьера без password")
    def test_create_courier_missing_password(self):
        payload = {"login": generate_random_string(), "firstName": generate_random_string()}
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 400

    @allure.title("Попытка создания дубликата курьера")
    def test_create_duplicate_courier(self):
        courier = register_new_courier_and_return_login_password()
        payload = {"login": courier["login"], "password": courier["password"], "firstName": courier["firstName"]}
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 409