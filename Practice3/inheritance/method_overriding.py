class Animal:
    def sound(self):
        print("Some sound")

class Cat(Animal):
    def sound(self): # Переопределение метода
        print("Meow")

my_cat = Cat()
my_cat.sound()