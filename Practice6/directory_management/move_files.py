# Перемещение файла
import shutil
import os

# Проверяем есть ли файл
if os.path.exists("example.txt"):
    shutil.move("example.txt", "test_dir/example.txt")
    print("Файл перемещён в test_dir")
else:
    print("Файл example.txt не найден")