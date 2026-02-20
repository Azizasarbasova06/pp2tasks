class Circle:
    pi = 3.14 # Переменная класса (общая для всех)

    def __init__(self, radius):
        self.radius = radius # Переменная экземпляра (у каждого своя)

c1 = Circle(5)
print(f"Area: {Circle.pi * (c1.radius ** 2)}")