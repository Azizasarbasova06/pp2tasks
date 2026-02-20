# Позиционные и именованные аргументы, аргументы по умолчанию
def describe_pet(pet_name, animal_type='dog'):
    print(f"I have a {animal_type} named {pet_name}.")

describe_pet("Buddy") # Использование дефолта
describe_pet(pet_name="Whiskers", animal_type="cat") # Именованные