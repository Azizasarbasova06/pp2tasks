import shutil
import os
    
# Копируем файл
shutil.copy("example.txt", "copy_example.txt")
print("Файл скопирован")

# Проверяем существует ли файл и удаляем
if os.path.exists("copy_example.txt"):
    os.remove("copy_example.txt")
    print("Файл удалён")
else:
    print("Файл не найден")