import pytest
import allure
from helpers.courier_helpers import register_new_courier_and_return_login_password
from helpers.api_helpers import login_courier, delete_courier

@pytest.fixture
def create_and_get_courier_data():
    # Создаем курьера
    login, password, first_name = register_new_courier_and_return_login_password()

    # Получаем ID курьера для удаления
    login_response = login_courier({"login": login, "password": password})
    courier_id = login_response.json()["id"]

    # Возвращаем данные в тест прямо сейчас
    yield login, password, first_name

    # Выполняется ПОСЛЕ теста (даже если тест упал!)
    delete_courier(courier_id)
