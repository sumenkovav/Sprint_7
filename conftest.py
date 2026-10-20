import pytest
import allure
from helpers.courier_helpers import register_new_courier_and_return_login_password
from helpers.api_helpers import login_courier, delete_courier


@pytest.fixture
def create_and_get_courier_data(request):
    login, password, first_name = register_new_courier_and_return_login_password()
    
    # Получаем ID курьера для удаления
    login_response = login_courier({"login": login, "password": password})
    courier_id = login_response.json()["id"]
    
    # Определяем функцию очистки
    def fin():
        delete_courier(courier_id)
    
    # Регистрируем функцию очистки для выполнения после теста
    request.addfinalizer(fin)
    
    # Возвращаем данные курьера
    return login, password, first_name

