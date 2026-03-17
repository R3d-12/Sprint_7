import pytest
import requests
import allure
import random
from utils.helpers import BASE_URL, generate_random_string

@allure.suite("API Заказов")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    @allure.title("Создание заказа с разными цветами")
    def test_create_order_with_colors(self, color):
        with allure.step(f"Формируем данные заказа с цветом: {color}"):
            order_data = {
                "firstName": generate_random_string(6),
                "lastName": generate_random_string(8),
                "address": f"{generate_random_string(5)} Street, 1",
                "metroStation": 1,
                "phone": f"+7{str(9000000000 + random.randint(0, 999999999))}",
                "rentTime": 2,
                "deliveryDate": "2026-03-15",
                "comment": "Test order",
                "color": color
            }

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(f"{BASE_URL}/orders", json=order_data, timeout=15)
            response.raise_for_status()
            data = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 201, f"Ожидался 201, получили {response.status_code}"

        with allure.step("Проверка тела ответа"):
            assert "track" in data, f"В ответе нет track: {data}"
            assert isinstance(data["track"], int) and data["track"] > 0, f"Некорректный track: {data}"