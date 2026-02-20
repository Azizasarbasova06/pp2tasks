class Mother:
    m_name = "Elena"

class Father:
    f_name = "Ivan"

class Child(Mother, Father): # Наследование от двоих
    def show_parents(self):
        print(f"Father: {self.f_name}, Mother: {self.m_name}")

c = Child()
c.show_parents()