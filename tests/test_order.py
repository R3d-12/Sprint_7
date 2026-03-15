import pytest
import requests
import allure
from utils.helpers import BASE_URL

@allure.suite("API Заказов")
@allure.feature("Создание заказа")
@pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
@allure.title("Создание заказа с разными цветами")
def test_create_order_with_colors(color):
    order_data = {
        "firstName": "Test",
        "lastName": "User",
        "address": "Test Street, 1",
        "metroStation": 1,
        "phone": "+70000000000",
        "rentTime": 2,
        "deliveryDate": "2026-03-15",
        "comment": "Test order",
        "color": color
    }
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    assert response.status_code == 201
    assert "track" in response.json()