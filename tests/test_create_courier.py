import allure
import pytest
from helpers.api_helpers import create_courier, login_courier
from data.test_data import CourierData
from helpers.generators import generate_random_login, generate_random_password, generate_random_first_name

@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера с валидными данными")
    @allure.step("Отправляем запрос на создание курьера")
    def test_create_courier_success(self):
        login = generate_random_login()
        password = generate_random_password()
        first_name = generate_random_first_name()

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        with allure.step("Отправляем POST-запрос на /api/v1/courier"):
            response = create_courier(payload)

        with allure.step("Проверяем код ответа 201"):
            assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"

        with allure.step("Проверяем, что ответ содержит {'ok': true}"):
            assert response.json() == {"ok": True}, f"Ожидался {{'ok': True}}, получен {response.json()}"

        with allure.step("Проверяем, что курьер действительно создан (можно авторизоваться)"):
            login_response = login_courier({"login": login, "password": password})
            assert login_response.status_code == 200, "Курьер не найден в системе"
            assert "id" in login_response.json(), "В ответе авторизации нет id"

    @allure.title("Нельзя создать двух одинаковых курьеров")
    @allure.step("Создаём курьера и пытаемся создать дубликат")
    def test_create_duplicate_courier_fails(self, create_and_get_courier_data):
        login, password, first_name = create_and_get_courier_data

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        with allure.step("Пытаемся создать курьера с теми же данными"):
            response = create_courier(payload)

        with allure.step("Проверяем код ответа 409 (Conflict)"):
            assert response.status_code == 409, f"Ожидался код 409, получен {response.status_code}"

        with allure.step("Проверяем текст ошибки"):
            expected_message = "Этот логин уже используется. Попробуйте другой."
            assert response.json()["message"] == expected_message, \
                f"Ожидалось сообщение '{expected_message}', получено {response.json()}"

    @allure.title("Проверка обязательных полей при создании курьера")
    @allure.step("Отправляем запрос без одного из обязательных полей")
    @pytest.mark.parametrize("missing_field, payload", CourierData.MISSING_FIELDS)
    def test_create_courier_missing_fields_fails(self, missing_field, payload):
        with allure.step(f"Пытаемся создать курьера без поля '{missing_field}'"):
            response = create_courier(payload)

        with allure.step("Проверяем код ответа 400 (Bad Request)"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

        with allure.step("Проверяем сообщение об ошибке"):
            expected_message = "Недостаточно данных для создания учетной записи"
            assert response.json()["message"] == expected_message, \
                f"Ожидалось сообщение '{expected_message}', получено {response.json()}"

    @allure.title("Создание курьера с уже существующим логином")
    @allure.step("Создаём курьера и пытаемся создать другого с тем же логином")
    def test_create_courier_with_existing_login_fails(self, create_and_get_courier_data):
        login, _, _ = create_and_get_courier_data

        new_password = generate_random_password()
        new_first_name = generate_random_first_name()

        payload = {
            "login": login,
            "password": new_password,
            "firstName": new_first_name
        }

        with allure.step("Пытаемся создать курьера с уже существующим логином"):
            response = create_courier(payload)

        with allure.step("Проверяем код ответа 409 (Conflict)"):
            assert response.status_code == 409, f"Ожидался код 409, получен {response.status_code}"

        with allure.step("Проверяем текст ошибки"):
            expected_message = "Этот логин уже используется. Попробуйте другой."
            assert response.json()["message"] == expected_message, \
                f"Ожидалось сообщение '{expected_message}', получено {response.json()}"
                       