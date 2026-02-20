class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

class Student(Person):
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname) # Вызов родителя
        self.graduation_year = year

s = Student("Aziza", "S", 2028)
print(s.graduation_year)