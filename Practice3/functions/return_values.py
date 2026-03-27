# 1. Расчет итогового балла
def get_final_score(quiz, midterm, final):
    return quiz + midterm + final

# 2. Проверка возможности заказа
def can_order(balance, total_cost):
    if balance >= total_cost:
        return True, balance - total_cost
    return False, balance

# 3. Генерация меню (возврат списка)
def generate_menu(base_dish):
    return [base_dish, f"{base_dish} с соусом", f"{base_dish} XL"]

# 4. Кортеж с минимальной и максимальной ценой
def get_price_range(prices):
    return min(prices), max(prices)

res, change = can_order(5000, 3200)
print(f"Заказ оформлен: {res}, Сдача: {change}")