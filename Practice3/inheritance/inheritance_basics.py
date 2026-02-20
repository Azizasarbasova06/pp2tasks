class Parent:
    def info(self):
        print("I am parent")

class Child(Parent):
    pass

c = Child()
c.info()