import allure
import pytest
from helpers.api_helpers import create_order
from data.test_data import OrderData


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цветов")
    @allure.step("Отправляем запрос на создание заказа")
    @pytest.mark.parametrize("color", OrderData.COLORS)
    def test_create_order_with_colors(self, color):
        
        payload = OrderData.BASE_ORDER.copy()
        payload["color"] = color  
        
        with allure.step(f"Отправляем POST-запрос с цветом: {color if color else 'без цвета'}"):
            response = create_order(payload)
        
        with allure.step("Проверяем код ответа 201"):
            assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
        
        with allure.step("Проверяем, что ответ содержит track"):
            assert "track" in response.json(), "Ответ не содержит track"
            assert response.json()["track"] is not None, "track не может быть пустым"
            
        with allure.step("Проверяем, что track — это число"):
            assert isinstance(response.json()["track"], int), "track должен быть числом"

            