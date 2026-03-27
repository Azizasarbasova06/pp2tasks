# 1. Смартфон (Телефон + Камера)
class PhonePart:
    def call(self): print("Calling...")

class CameraPart:
    def photo(self): print("Click!")

class Smartphone(PhonePart, CameraPart):
    pass

# 2. Студент-разработчик
class Learner:
    def study(self): print("Studying PP2")

class Coder:
    def write_code(self): print("Writing Python")

class TechStudent(Learner, Coder):
    pass

# 3. Робот-пылесос (Пылесос + ИИ)
class Vacuum:
    def clean(self): print("Cleaning floors")

class AI:
    def think(self): print("Calculating path")

class RoboCleaner(Vacuum, AI):
    pass

# 4. Многофункциональное устройство (Принтер + Сканер)
class Printer:
    def print_doc(self): print("Printing")

class Scanner:
    def scan_doc(self): print("Scanning")

class MFU(Printer, Scanner):
    pass