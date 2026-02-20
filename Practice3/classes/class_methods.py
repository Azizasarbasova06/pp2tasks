# 1. Кошелек с методами транзакций
class Wallet:
    def __init__(self, balance):
        self.balance = balance
    def add(self, amount):
        self.balance += amount
    def get_info(self):
        return f"Баланс: {self.balance} KZT"

# 2. Система управления заказом
class OrderStatus:
    def __init__(self, order_id):
        self.id = order_id
        self.state = "Pending"
    def complete(self):
        self.state = "Completed"

# 3. Калькулятор для SIS
class ShopCalc:
    def multiply(self, a, b):
        return a * b

# 4. Робот-помощник
class Assistant:
    def greet(self, user):
        print(f"Hello, {user}! I am your KBTU assistant.")

w = Wallet(1000)
w.add(500)
print(w.get_info())