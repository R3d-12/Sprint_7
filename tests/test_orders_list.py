import requests
import allure
from utils.helpers import BASE_URL

@allure.suite("API Заказов")
@allure.feature("Получение списка заказов")
class TestGetOrders:

    @allure.title("Получение списка всех заказов")
    def test_get_orders_list(self):
        with allure.step("Отправка запроса на получение всех заказов"):
            response = requests.get(f"{BASE_URL}/orders")
            data = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"

        with allure.step("Проверка, что orders — это список"):
            assert isinstance(data.get("orders"), list), f"Ожидался список, получили: {data.get('orders')}"