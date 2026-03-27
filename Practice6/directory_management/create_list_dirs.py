import os

# Создаём папку если её нет
if not os.path.exists("test_dir"):
    os.mkdir("test_dir")
    print("Папка test_dir создана")
else:
    print("Папка уже существует")

# Создаём вложенные папки
os.makedirs("parent/child", exist_ok=True)
print("Вложенные папки созданы")

# Показываем список файлов и папок
print("Содержимое папки:")
print(os.listdir())

# Текущая директория
print("Текущая папка:")
print(os.getcwd())