import allure
import pytest
from helpers.api_helpers import create_courier, login_courier
from data.test_data import CourierData


@allure.feature("Авторизация курьера")
class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    @allure.step("Создаём курьера и авторизуемся")
    def test_login_success(self, create_and_get_courier_data):
        login, password, _ = create_and_get_courier_data
        
        payload = {
            "login": login,
            "password": password
        }
        
        with allure.step("Отправляем POST-запрос на /api/v1/courier/login"):
            response = login_courier(payload)
        
        with allure.step("Проверяем код ответа 200"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        
        with allure.step("Проверяем, что в ответе есть id"):
            assert "id" in response.json(), "Ответ не содержит id"
            assert response.json()["id"] is not None, "id не может быть пустым"

    @allure.title("Авторизация с неверным логином")
    @allure.step("Отправляем запрос с неверным логином")
    def test_login_wrong_login_fails(self, create_and_get_courier_data):
        _, password, _ = create_and_get_courier_data
        
        payload = {
            "login": CourierData.INVALID_LOGIN,
            "password": password
        }
        
        with allure.step("Отправляем POST-запрос с неправильным логином"):
            response = login_courier(payload)
        
        with allure.step("Проверяем код ответа 404"):
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"
        
        with allure.step("Проверяем сообщение об ошибке"):
            expected_message = "Учетная запись не найдена"
            assert response.json()["message"] == expected_message, \
                f"Ожидалось сообщение '{expected_message}', получено {response.json()}"

    @allure.title("Авторизация с неверным паролем")
    @allure.step("Отправляем запрос с неверным паролем")
    def test_login_wrong_password_fails(self, create_and_get_courier_data):
        login, _, _ = create_and_get_courier_data
        
        payload = {
            "login": login,
            "password": CourierData.INVALID_PASSWORD
        }
        
        with allure.step("Отправляем POST-запрос с неправильным паролем"):
            response = login_courier(payload)
        
        with allure.step("Проверяем код ответа 404"):
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"
        
        with allure.step("Проверяем сообщение об ошибке"):
            expected_message = "Учетная запись не найдена"
            assert response.json()["message"] == expected_message, \
                f"Ожидалось сообщение '{expected_message}', получено {response.json()}"

    @allure.title("Авторизация несуществующего пользователя")
    @allure.step("Отправляем запрос с несуществующими логином и паролем")
    def test_login_nonexistent_user_fails(self):
        payload = {
            "login": CourierData.LOGIN_PAYLOADS["nonexistent"]["login"],
            "password": CourierData.LOGIN_PAYLOADS["nonexistent"]["password"]
        }
        
        with allure.step("Отправляем POST-запрос с несуществующими данными"):
            response = login_courier(payload)
        
        with allure.step("Проверяем код ответа 404"):
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"
        
        with allure.step("Проверяем сообщение об ошибке"):
            expected_message = "Учетная запись не найдена"
            assert response.json()["message"] == expected_message, \
                f"Ожидалось сообщение '{expected_message}', получено {response.json()}"

    @allure.title("Проверка обязательных полей при авторизации")
    @allure.step("Отправляем запрос без одного из обязательных полей")
    @pytest.mark.parametrize("missing_field, payload", CourierData.MISSING_LOGIN_FIELDS)
    def test_login_missing_fields_fails(self, missing_field, payload):
        with allure.step(f"Пытаемся авторизоваться без поля '{missing_field}'"):
            response = login_courier(payload)
        
        with allure.step("Проверяем код ответа 400"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
        
        with allure.step("Проверяем сообщение об ошибке"):
            expected_message = "Недостаточно данных для входа"
            assert response.json()["message"] == expected_message, \
                f"Ожидалось сообщение '{expected_message}', получено {response.json()}"