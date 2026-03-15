import requests
import allure
from utils.helpers import BASE_URL

@allure.suite("API Заказов")
@allure.feature("Получение списка заказов")
@allure.title("Получение списка всех заказов")
def test_get_orders_list():
    response = requests.get(f"{BASE_URL}/orders")
    assert response.status_code == 200
    assert isinstance(response.json().get("orders"), list)