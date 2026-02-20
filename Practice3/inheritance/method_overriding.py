# 1. Звуки
class Dog:
    def sound(self): print("Bark")
class Puppy(Dog):
    def sound(self): print("Small bark")
# 2. Платежи
class Pay:
    def go(self): print("Generic")
class Cash(Pay):
    def go(self): print("Cash pay")
# 3. Скорость
class Runner:
    def speed(self): print("Slow")
class Pro(Runner):
    def speed(self): print("Fast")
# 4. Приветствие
class Human:
    def say(self): print("Hi")
class Kaz(Human):
    def say(self): print("Salem")