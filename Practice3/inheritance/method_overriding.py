# 1. Переопределение приветствия
class Human:
    def greet(self): print("Hello")

class LocalStudent(Human):
    def greet(self): print("Салем! Калайсын?")

# 2. Звуки разных объектов
class Alarm:
    def ring(self): print("Beep beep")

class SchoolBell(Alarm):
    def ring(self): print("DING DING DING!")

# 3. Разные типы доставки
class StandardShipping:
    def process(self): print("Delivery in 3 days")

class ExpressShipping(StandardShipping):
    def process(self): print("Delivery in 2 hours!")

# 4. Формат вывода данных
class Reporter:
    def report(self, data): print(f"Raw: {data}")

class JSONReporter(Reporter):
    def report(self, data): print(f"JSON: {{'data': '{data}'}}")

kaspi_ship = ExpressShipping()
kaspi_ship.process()