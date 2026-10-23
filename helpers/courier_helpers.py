import requests
from helpers.generators import generate_random_login, generate_random_password, generate_random_first_name

def register_new_courier_and_return_login_password():
    # Генерируем данные через импортированные функции
    login = generate_random_login()
    password = generate_random_password()
    first_name = generate_random_first_name()

    login_pass = []

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass