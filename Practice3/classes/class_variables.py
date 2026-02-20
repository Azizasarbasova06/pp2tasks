# 1. Общий налог маркетплейса
class SIS_Store:
    tax = 0.12 # 12% общая переменная класса
    def __init__(self, price):
        self.final_price = price * (1 + SIS_Store.tax)

# 2. Счетчик студентов на курсе
class PP2_Course:
    student_count = 0
    def __init__(self, name):
        self.name = name
        PP2_Course.student_count += 1

# 3. Константы университета
class KBTU_Info:
    founded = 2001
    domain = "kbtu.kz"

# 4. Версия приложения
class AppSettings:
    version = "1.0.4-stable"

s1 = PP2_Course("Aziza")
s2 = PP2_Course("Ali")
print(f"Всего студентов: {PP2_Course.student_count}")