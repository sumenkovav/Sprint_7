import random
import string


# Генераторы случайных данных
@staticmethod
def generate_random_login():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))
    
@staticmethod
def generate_random_password():
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(10))
    
@staticmethod
def generate_random_first_name():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

