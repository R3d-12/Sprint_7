import pytest
import requests
import allure
from utils.helpers import register_new_courier_and_return_login_password, BASE_URL, generate_random_string

@allure.suite("API Курьеров")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        with allure.step("Регистрация нового курьера"):
            response, courier_data = register_new_courier_and_return_login_password()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}"

        with allure.step("Проверка тела ответа"):
            assert response.json().get("ok") is True, f"Некорректное тело ответа: {response.json()}"

    @allure.title("Попытка создания курьера без обязательного поля")
    @pytest.mark.parametrize(
        "payload",
        [
            {"password": generate_random_string()},
            {"login": generate_random_string(), "firstName": generate_random_string()},
        ],
    )
    def test_create_courier_missing_required_fields(self, payload):
        with allure.step(f"Отправка запроса с данными: {payload}"):
            response = requests.post(f"{BASE_URL}/courier", json=payload)
            body = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert body["message"] == "Недостаточно данных для создания учетной записи", f"Некорректное сообщение: {body}"

    @allure.title("Попытка создания дубликата курьера")
    def test_create_duplicate_courier(self):
        with allure.step("Создание исходного курьера"):
            response, courier_data = register_new_courier_and_return_login_password()

        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"],
            "firstName": courier_data["firstName"]
        }

        with allure.step("Попытка создания курьера с тем же логином"):
            duplicate_response = requests.post(f"{BASE_URL}/courier", json=payload)

        with allure.step("Проверка кода ответа при дубликате"):
            assert duplicate_response.status_code == 409, f"Ожидали 409, получили {duplicate_response.status_code}"

        with allure.step("Проверка сообщения об ошибке при дубликате"):
            assert duplicate_response.json().get("message") == "Этот логин уже используется. Попробуйте другой.", \
                f"Некорректное сообщение: {duplicate_response.json()}"