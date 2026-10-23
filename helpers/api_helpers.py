import allure
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

# Функции для курьера
@allure.step("Отправляем запрос на создание курьера")
def create_courier(payload):
    return requests.post(f"{BASE_URL}/courier", data=payload)  # Для курьера оставляем data=

@allure.step("Отправляем запрос на логин курьера")
def login_courier(payload):
    return requests.post(f"{BASE_URL}/courier/login", data=payload)  # Для логина оставляем data=

# Функции для заказов
@allure.step("Отправляем запрос на создание заказа")
def create_order(payload):
    return requests.post(f"{BASE_URL}/orders", json=payload)  # ← Меняем data= на json=

@allure.step("Отправляем запрос на получение списка заказов")
def get_orders():
    return requests.get(f"{BASE_URL}/orders")

# Дополнительные функции
@allure.step("Отправляем запрос на получение списка курьеров (если есть)")
def get_couriers():
    return requests.get(f"{BASE_URL}/courier")

@allure.step("Отправляем запрос на удаление курьера (если есть)")
def delete_courier(courier_id):
    return requests.delete(f"{BASE_URL}/courier/{courier_id}")