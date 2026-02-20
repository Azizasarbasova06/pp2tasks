# 1. Базовый super
class A:
    def __init__(self): print("A")
class B(A):
    def __init__(self): super().__init__(); print("B")
# 2. Super с данными
class Person:
    def __init__(self, name): self.name = name
class Student(Person):
    def __init__(self, name, id): super().__init__(name); self.id = id
# 3. Super в методах
class X:
    def show(self): print("X")
class Y(X):
    def show(self): super().show(); print("Y")
# 4. Super с ценами
class Item:
    def __init__(self, p): self.p = p
class Toy(Item):
    def __init__(self, p, t): super().__init__(p); self.t = t