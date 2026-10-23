
import string

class CourierData:
    # Невалидные данные (для тестов ошибок)
    INVALID_LOGIN = "не_существующий"
    INVALID_PASSWORD = "wrong_pass"
    
    # Данные для параметризации тестов логина
    LOGIN_PAYLOADS = {
        "invalid_login": {"login": INVALID_LOGIN, "password": "Qwerty123"},
        "invalid_password": {"login": "test_courier", "password": INVALID_PASSWORD},
        "nonexistent": {"login": "user_not_exist", "password": "pass_not_exist"}
    }
    
    MISSING_LOGIN_FIELDS = [
        ("login", {"password": "Qwerty123"}),       # нет логина
        ("password", {"login": "test_courier", "password": ""})  # нет пароля
    ]

    
    # Данные для параметризации тестов создания курьера
    MISSING_FIELDS = [
        ("login", {"password": "Qwerty123", "firstName": "Александр"}),      # нет login
        ("password", {"login": "test_user", "firstName": "Александр"})     # нет password
    ]

class OrderData:
    COLORS = [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []  
    ]
    
    BASE_ORDER = {
        "firstName": "Александр",
        "lastName": "Пушкин",
        "address": "ул. Писателя, 1",
        "metroStation": 1,
        "phone": "+79991112233",
        "rentTime": 5,
        "deliveryDate": "2026-10-20",
        "comment": "Тест",
        "color": [] 
    }  