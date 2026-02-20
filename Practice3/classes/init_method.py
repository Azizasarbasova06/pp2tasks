class Student:
    def __init__(self, name, id):
        self.name = name
        self.id = id

s1 = Student("Aziza", "24B123")
print(f"Student: {s1.name}, ID: {s1.id}")