import allure
from helpers.api_helpers import get_orders


@allure.feature("Список заказов")
class TestOrdersList:

    @allure.title("Проверка, что тело ответа содержит список заказов")
    @allure.step("Отправляем GET-запрос на /api/v1/orders")
    def test_orders_list_returns_list(self):
        with allure.step("Отправляем запрос на получение списка заказов"):
            response = get_orders()

        with allure.step("Проверяем код ответа 200"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        with allure.step("Проверяем, что тело ответа — это словарь"):
            data = response.json()
            assert isinstance(data, dict), f"Ожидался словарь, получен {type(data)}"

        with allure.step("Проверяем, что в ответе есть ключ 'orders'"):
            assert "orders" in data, "В ответе отсутствует ключ 'orders'"

        with allure.step("Проверяем, что 'orders' — это список"):
            orders = data["orders"]
            assert isinstance(orders, list), f"Ожидался список, получен {type(orders)}"

        with allure.step("Проверяем, что список содержит хотя бы один заказ (опционально)"):
            assert len(orders) > 0, "Список заказов не должен быть пустым"
             